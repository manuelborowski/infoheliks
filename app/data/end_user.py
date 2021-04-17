from app.data.models import EndUser
from app.data import utils as mutils, end_user as mend_user
import random, string, datetime
from app import log, db


def create_random_string(len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))


class Profile(EndUser.Profile):
    pass


def add_end_user(first_name, last_name, email, profile, code):
    try:
        user = EndUser(first_name=first_name, last_name=last_name, email=email, profile=profile, code=code)
        db.session.add(user)
        db.session.commit()
        log.info(f'Enduser {user.full_name()} added')
        return user
    except Exception as e:
        mutils.raise_error('could not add end user', e)
    return None


def delete_end_user(id=None, id_list=None):
    try:
        if id:
            id_list = [id]
        for id in id_list:
            user = get_first_end_user(id=id)
            db.session.delete(user)
        db.session.commit()
        log.info('end user deleted')
    except Exception as e:
        mutils.raise_error('could not delete end user', e)


def get_end_users(email=None, profile=None, code=None, id=None, first=False):
    try:
        users = EndUser.query
        if email:
            users = users.filter(EndUser.email == email)
        if profile:
            users = users.filter(EndUser.profile == profile)
        if code:
            users = users.filter(EndUser.code == code)
        if id:
            users = users.filter(EndUser.id == id)
        if first:
            user = users.first()
            return user
        users = users.all()
        return users
    except Exception as e:
        mutils.raise_error('could not get end users', e)
    return None


def get_first_end_user(email=None, profile=None, code=None, id=None):
    return get_end_users(email=email, profile=profile, code=code, id=id, first=True)


def update_end_user(user, end_user=None, first_name=None, last_name=None, email=None, profile=None):
    try:
        if end_user:
            user.end_users.append(end_user)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if profile:
            user.profile = profile
        db.session.commit()
        return user
    except Exception as e:
        mutils.raise_error(f'could not update end user {user.full_name()}', e)
    return None


def update_email_sent_by_id(id, value):
    try:
        end_user = EndUser.query.get(id)
        end_user.set_email_sent(value)
        log.info(f'end_user email-sent update {id} {value}')
        return end_user
    except Exception as e:
        mutils.raise_error(f'could not update end_user email-sent {id} {value}', e)
    return None


def update_survey_email_sent_by_id(id, value):
    try:
        end_user = EndUser.query.get(id)
        end_user.set_survey_email_sent(value)
        log.info(f'end_user survey-email-sent update {id} {value}')
        return end_user
    except Exception as e:
        mutils.raise_error(f'could not update end_user email-sent {id} {value}', e)
    return None


def update_enable_by_id(id, value):
    try:
        end_user = EndUser.query.get(id)
        end_user.set_enabled(value)
        db.session.commit()
        log.info(f'end_user enable update {id} {value}')
        return end_user
    except Exception as e:
        mutils.raise_error(f'could not update end_user enable {id} {value}', e)
    return None


def update_email_send_retry_by_id(id, value):
    try:
        end_user = EndUser.query.get(id)
        end_user.set_email_send_retry(value)
        log.info(f'registration email-send-retry update {id} {value}')
        return end_user
    except Exception as e:
        mutils.raise_error(f'could not update registration email-send-retry {id} {value}', e)
    return None


def subscribe_ack_email_sent(cb, opaque):
    return EndUser.subscribe_ack_email_sent(cb, opaque)


def subscribe_survey_email_sent(cb, opaque):
    return EndUser.subscribe_survey_email_sent(cb, opaque)


def subscribe_email_send_retry(cb, opaque):
    return EndUser.subscribe_email_send_retry(cb, opaque)


def subscribe_enabled(cb, opaque):
    return EndUser.subscribe_enabled(cb, opaque)


def get_first_not_sent_registration():
    end_user = EndUser.query.filter(EndUser.enabled)
    end_user = end_user.filter(not EndUser.email_sent)
    end_user = end_user.first()
    return end_user


def get_first_not_sent_survey():
    end_user = EndUser.query.filter(EndUser.enabled)
    end_user = end_user.filter(not EndUser.survey_email_sent)
    end_user = end_user.first()
    return end_user


def pre_filter():
    return db.session.query(EndUser)


def search_data(search_string):
    search_constraints = []
    # search_constraints.append(EndUser.email.like(search_string))
    # search_constraints.append(EndUser.first_name.like(search_string))
    # search_constraints.append(EndUser.last_name.like(search_string))
    # search_constraints.append(EndUser.profile.like(search_string))
    # search_constraints.append(EndUser.sub_profile.like(search_string))
    # search_constraints.append(Visit.timeslot.like(search_string))
    return search_constraints


def format_data(db_list):
    out = []
    # for i in db_list:
    #     survey = i.ret_dict()
    #     em = json.loads(survey['result'])
    #     em['row_action'] = f"{i.id}"
    #     em['id'] = f"{i.id}"
    #     em['DT_RowId'] = f"{i.id}"
    #     out.append(em)
    return out
