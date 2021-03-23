from app import db, log
from app.data import utils as mutils
from app.data.models import Visit, EndUser


def add_visit(timeslot, code):
    try:
        visit = Visit(code=code, timeslot=timeslot)
        db.session.add(visit)
        db.session.commit()
        log.info(f'visit added: {timeslot}')
        return visit
    except Exception as e:
        mutils.raise_error('could not add visit', e)
    return None


def update_visit(visit, timeslot=None, code=None, room_code=None, survey_email_send_retry=None):
    try:
        if timeslot:
            visit.timeslot = timeslot
        if code:
            visit.code = code
        if room_code:
            visit.room_code = room_code
        if survey_email_send_retry:
            visit.survey_email_send_retry = survey_email_send_retry
        db.session.commit()
        log.info(f'visit updated : {visit}')
        return visit
    except Exception as e:
        mutils.raise_error('could not update visit', e)
    return None


def delete_visit(code=None, id=None):
    try:
        visit = get_first_visit(code=code, id=id)
        db.session.delete(visit)
        db.session.commit()
        log.info(f'visit deleted: {code}')
    except Exception as e:
        mutils.raise_error('could not delete visit', e)


def get_visits(user=None, timeslot=None, code=None, id=None, room_code=None, first_visit=False, count=False, room_code_present=False, survey_email_send_retry=None):
    try:
        visits =Visit.query
        if user:
            visits = visits.filter(Visit.end_user == user)
        if timeslot:
            visits = visits.filter(Visit.timeslot == timeslot)
        if code:
            visits = visits.filter(Visit.code == code)
        if survey_email_send_retry:
            visits = visits.filter(Visit.survey_email_send_retry == survey_email_send_retry)
        if room_code:
            visits = visits.filter(Visit.room_code == room_code)
        if id:
            visits = visits.filter(Visit.id == id)
        if room_code_present:
            visits = visits.filter(Visit.room_code != None)
        if first_visit:
            visit = visits.first()
            return visit
        elif count:
            visit_count = visits.count()
            return visit_count
        visits = visits.all()
        return visits
    except Exception as e:
        mutils.raise_error('could not get visit', e)
    return None



def get_first_visit(user=None, timeslot=None, code=None, id=None, room_code=None):
    visit = get_visits(user, timeslot, code, id, room_code, first_visit=True)
    return visit


def get_visit_count(timeslot=None):
    count = get_visits(timeslot=timeslot, count=True)
    return count


def update_email_sent_by_id(id, value):
    try:
        visit = Visit.query.get(id)
        visit.set_email_sent(value)
        log.info(f'visit email-sent update {id} {value}')
        return visit
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id} {value}', e)
    return None


def update_survey_email_sent_by_id(id, value):
    try:
        visit = Visit.query.get(id)
        visit.set_survey_email_sent(value)
        log.info(f'visit survey-email-sent update {id} {value}')
        return visit
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id} {value}', e)
    return None


def update_enable_by_id(id, value):
    try:
        visit = Visit.query.get(id)
        visit.set_enabled(value)
        db.session.commit()
        log.info(f'visit enable update {id} {value}')
        return visit
    except Exception as e:
        mutils.raise_error(f'could not update visit enable {id} {value}', e)
    return None


def update_email_send_retry_by_id(id, value):
    try:
        visit = Visit.query.get(id)
        visit.set_email_send_retry(value)
        log.info(f'registration email-send-retry update {id} {value}')
        return visit
    except Exception as e:
        mutils.raise_error(f'could not update registration email-send-retry {id} {value}', e)
    return None


def subscribe_ack_email_sent(cb, opaque):
    return Visit.subscribe_ack_email_sent(cb, opaque)


def subscribe_survey_email_sent(cb, opaque):
    return Visit.subscribe_survey_email_sent(cb, opaque)


def subscribe_email_send_retry(cb, opaque):
    return Visit.subscribe_email_send_retry(cb, opaque)


def subscribe_enabled(cb, opaque):
    return Visit.subscribe_enabled(cb, opaque)


def get_first_not_sent_registration():
    visit = Visit.query.filter(Visit.enabled)
    visit = visit.filter(Visit.email_sent == False)
    visit = visit.first()
    return visit


def get_first_not_sent_survey():
    visit = Visit.query.filter(Visit.enabled)
    visit = visit.filter(Visit.survey_email_sent == False)
    visit = visit.filter(Visit.room_code != None)
    visit = visit.filter(Visit.room_code != '')
    visit = visit.first()
    return visit







