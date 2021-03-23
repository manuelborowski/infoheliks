from app import log
from app.data import utils as mutils, floor as mfloor


def add_floor(level, name='', info='', has_chat=False):
    try:
        floor = mfloor.get_first_floor(level=level)
        if floor:
            log.warning(f'Floor {level} {name} already exists')
            return floor
        floor = mfloor.add_floor(level, name, info, has_chat=has_chat)
    except Exception as e:
        mutils.raise_error(f'could not add floor {level}', e)
    return floor


def get_floors():
    return mfloor.get_floors()


add_floor('CLB', 'CLB')
add_floor('Scholengemeenschap', 'Scholengemeenschap', has_chat=True)
add_floor('Internaat', 'Internaat')