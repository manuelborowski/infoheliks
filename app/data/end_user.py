from app.data.models import EndUser, Visit, Fair, Floor
from app.data import utils as mutils, visit as mvisit
import random, string, datetime
from app import log, db


def create_random_string(len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))


class Profile(EndUser.Profile):
    pass


class School(Fair.School):
    pass


class Level(Floor.Level):
    pass


def add_end_user(first_name, last_name, email, profile, sub_profile):
    try:
        user = EndUser(first_name=first_name, last_name=last_name, email=email, profile=profile, sub_profile=sub_profile)
        db.session.add(user)
        db.session.commit()
        log.info(f'Enduser {user.full_name()} added')
        return user
    except Exception as e:
        mutils.raise_error('could not add end user', e)
    return None


def delete_end_user(code=None, user=None):
    try:
        if not user:
            user = get_first_end_user(code=code)
        db.session.delete(user)
        db.session.commit()
        log.info(f'end user deleted: {code}')
    except Exception as e:
        mutils.raise_error('could not delete end user', e)


def get_end_users(email=None, profile=None, sub_profile=None, code=None, first=False):
    try:
        users = EndUser.query
        if email:
            users = users.filter(EndUser.email == email)
        if profile:
            users = users.filter(EndUser.profile == profile)
        if sub_profile:
            users = users.filter(EndUser.sub_profile == sub_profile)
        if code:
            users = users.join(Visit).filter(Visit.code == code)
        if first:
            user = users.first()
            return user
        users = users.all()
        return users
    except Exception as e:
        mutils.raise_error('could not get end users', e)
    return None


def get_first_end_user(email=None, profile=None, sub_profile=None, code=None):
    return get_end_users(email=email, profile=profile, sub_profile=sub_profile, code=code, first=True)


def update_end_user(user, visit=None, first_name=None, last_name=None, email=None, profile=None, sub_profile=None):
    try:
        if visit:
            user.visits.append(visit)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if profile:
            user.profile = profile
        if sub_profile:
            user.sub_profile = sub_profile
        db.session.commit()
        return user
    except Exception as e:
        mutils.raise_error(f'could not update end user {user.full_name()}', e)
    return None


