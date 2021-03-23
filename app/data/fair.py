from app import db, log
from app.data.models import Fair
from app.data import utils as mutils

def add_fair(school, wonder):
    try:
        fair = Fair(school=school, wonder_url=wonder)
        db.session.add(fair)
        db.session.commit()
        return fair
    except Exception as e:
        mutils.raise_error(f'could not add fair {school}', e)
    return None


def update_fair(fair, school=None, wonder=None):
    try:
        if school:
            fair.school = school
        if wonder:
            fair.wonder_url = wonder
        db.session.commit()
        return fair
    except Exception as e:
        mutils.raise_error(f'could not update fair {fair}', e)
    return None


def get_fairs():
    try:
        fairs = Fair.query.filter().all()
        return fairs
    except Exception as e:
        mutils.raise_error(f'could not get fairs', e)
    return None


def get_first_fair(id=None, school=None):
    try:
        fair = Fair.query
        if id is not None:
            fair = fair.filter(Fair.id == id)
        if school is not None:
            fair = fair.filter(Fair.school == school)
        fair = fair.first()
        return fair
    except Exception as e:
        mutils.raise_error(f'could not get first fair', e)
    return None


def pre_filter():
    return db.session.query(Fair)


def search_data(search_string):
    search_constraints = []
    return search_constraints


def format_data(db_list):
    out = []
    for i in db_list:
        em = i.ret_dict()
        em['row_action'] = f"{i.id}"
        out.append(em)
    return out




# De chatbox geldt enkel voor scholengemeenschap en niet meer voor SAL internaat en CLB.
# De wonderkamers: SAL internaat – CLB – SAL – DR - SGC – Campus Sint-Ursula – VTI. Schoolmedewerkers moeten inderdaad een keuze maken.

