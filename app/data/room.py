from app.data.models import Room, Floor, EndUser, ChatLine
from app.data import utils as mutils
from app import db, log
import datetime

def get_rooms(code=None, floor=None):
    try:
        rooms = Room.query
        if code:
            rooms = rooms.filter(Room.code == code)
        if floor:
            rooms = rooms.filter(Room.floor == floor)
        rooms = rooms.all()
        return rooms
    except Exception as e:
        mutils.raise_error(f'could not find room for code {code}', e)
    return []


def get_first_room(code=None, floor=None):
    try:
        rooms = get_rooms(code=code, floor=floor)
        if rooms:
            return rooms[0]
    except Exception as e:
        mutils.raise_error(f'could not find room for code {code}', e)
    return None


def add_room(code, floor, name):
    room = None
    try:
        room = Room(code=code, floor=floor, name=name)
        db.session.add(room)
        db.session.commit()
    except Exception as e:
        mutils.raise_error(f'could not add room: ', e)
    return room


def update_room(room, nbr_guests=None):
    try:
        if nbr_guests:
            room.nbr_guests = nbr_guests
        db.session.commit()
    except Exception as e:
        mutils.raise_error(f'could not update room: ', e)
    return room


def delete_room(room):
    try:
        db.session.delete(room)
        db.session.commit()
    except Exception as e:
        mutils.raise_error(f'could not delete room: ', e)
    return room


def add_chat_line(room_code, sender_code, name, initials, text):
    try:
        room = Room.query.filter(Room.code == room_code).first()
        if room:
            chat_line = ChatLine(owner_code=sender_code, full_name=name, initials=initials, text=text, timestamp=datetime.datetime.now(), room=room)
            db.session.add(chat_line)
            db.session.commit()
        else:
            log.error(f'add_chat_line: room with wode {room_code} not found')
    except Exception as e:
        mutils.raise_error(f'could not add chat line', e)
    return None


def get_chat_line_count(room_code):
    try:
        room = Room.query.filter(Room.code == room_code).first()
        chat_line_count = ChatLine.query.filter(ChatLine.room_id==room.id).count()
        return chat_line_count
    except Exception as e:
        mutils.raise_error(f'could not get chat line count', e)
    return 0


def get_history(room_code):
    history = []
    try:
        room = Room.query.join(ChatLine).filter(Room.code == room_code).order_by(ChatLine.timestamp).first()
        if room:
            history = [{'room': room.code, 'sender': l.owner_code, 'name': l.full_name, 'initials': l.initials, 'text': l.text} for l in  room.history]
        return history
    except Exception as e:
        mutils.raise_error(f'could not get history for for room code {room_code}', e)
    return history

