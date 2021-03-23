from app import db, log
from app.data.models import Floor
from app.data import utils as mutils

def add_floor(level, name='', info='', has_chat=False):
    try:
        floor = Floor(level=level, name=name, info=info, has_chat=has_chat)
        db.session.add(floor)
        db.session.commit()
    except Exception as e:
        mutils.raise_error(f'could not add floor {level}', e)
    return floor


def get_floors(has_chat=None):
    try:
        floors = Floor.query
        if has_chat:
            floors = floors.filter(Floor.has_chat == has_chat)
        floors = floors.all()
        return floors
    except Exception as e:
        mutils.raise_error(f'could not get floors', e)
    return None


def get_first_floor(id=None, level=None):
    try:
        floor = Floor.query
        if id is not None:
            floor = floor.filter(Floor.id == id)
        if level is not None:
            floor = floor.filter(Floor.level == level)
        floor = floor.first()
        return floor
    except Exception as e:
        mutils.raise_error(f'could not get first floor', e)
    return None
