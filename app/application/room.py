from app.data import utils as mutils, room as mroom, end_user as mend_user, visit as mvisit, floor as mfloor
from app import db, log


def select_least_occupied_room(floor_level):
    try:
        unfiltered_rooms = mroom.get_rooms(floor=floor_level)
        rooms = []
        for room in unfiltered_rooms:
            visit = mvisit.get_first_visit(code=room.code)
            if visit.enabled:
                rooms.append(room)
        if rooms:
            max_count = 0
            min_count = 1000000
            selected_room = rooms[0]
            for room in rooms:
                count = mroom.get_chat_line_count(room.code)
                if max_count < count: max_count = count
                if min_count > count:
                    min_count = count
                    selected_room = room
            if (max_count - min_count) < 10:
                nbr_guests = 1000  # arbitrary large number
                selected_room = rooms[0]
                for room in rooms:
                    if room.nbr_guests < nbr_guests:
                        nbr_guests = room.nbr_guests
                        selected_room = room
                mroom.update_room(selected_room, nbr_guests=nbr_guests + 1)
            return selected_room
    except Exception as e:
        mutils.raise_error(f'could not get room with least number of guests for {floor_level}', e)
    return None


def add_guest_to_room(room, user_code):
    try:
        user = mend_user.get_first_end_user(code=user_code)
        mroom.update_room(room, user)
        return room
    except Exception as e:
        mutils.raise_error(f'could not add guest to room', e)
    return None


def get_chat_room_configuration(id, flat_user):
    try:
        split_id = id.split('-')
        level = split_id[0]
        select = split_id[1]
        if select == 'leastguests':
            if flat_user['is_guest']:
                if flat_user['room_code']:
                    room = mroom.get_first_room(code=flat_user['room_code'])
                else:
                    room = select_least_occupied_room(level)
                    visit = mvisit.get_first_visit(code=flat_user['code'])
                    visit.set_email_send_retry(0)
                    mvisit.update_visit(visit, room_code=room.code)
                return room.name, room.code
            return 'Lege kamer', 'NA'
        if flat_user['is_guest']:
            return 'Lege kamer', 'NA'
        rooms = mroom.get_rooms(floor=level)
        room = rooms[int(select)]
        visit = mvisit.get_first_visit(code=room.code)
        if visit.enabled:
            return room.name, room.code
    except Exception as e:
        log.error(f'configure chatroom error: {e}')
    return 'Lege kamer', 'NA'


def get_chat_rooms_history():
    try:
        chat_history = []
        rooms = mroom.get_rooms()
        for room in rooms:
            history = mroom.get_history(room.code)
            chat_history += history
        return chat_history
    except Exception as e:
        log.error(f'get chatrooms history error: {e}')
    return []


# Chatrooms are created when the appropriate coworker has registered.  But if the registration has been done
# before this code was released, no chatrooms are created.
def add_rooms_if_required():
    floors = mfloor.get_floors(has_chat=True)
    for floor in floors:
        users = mend_user.get_end_users(sub_profile=floor.level)
        for user in users:
            visit = mvisit.get_first_visit(user=user)
            room = mroom.get_first_room(code=visit.code)
            if not room:
                room = mroom.add_room(code=visit.code, floor=floor.level, name=user.full_name())

add_rooms_if_required()