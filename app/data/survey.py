from app import log, db
from app.data.models import EndUserSurvey, EndUser
from app.data import utils as mutils
import json


def add_survey(code, data):
    try:
        survey = EndUserSurvey(code=code, result=data)
        db.session.add(survey)
        db.session.commit()
        log.info(f'Survey {code} added')
        return survey
    except Exception as e:
        mutils.raise_error('could not add survey', e)
    return None


def update_survey(survey, data=None):
    try:
        if data:
            survey.result = data
        db.session.commit()
        return survey
    except Exception as e:
        mutils.raise_error('could not update survey', e)
    return None


def get_surveys(code=None, first=False):
    try:
        surveys = EndUserSurvey.query
        if code:
            surveys = surveys.filter(EndUserSurvey.code == code)
        if first:
            survey = surveys.first()
            return survey
        surveys = surveys.all()
        return surveys
    except Exception as e:
        mutils.raise_error('could not get surveys', e)
    return None


def get_first_survey(code=None):
    try:
        survey = get_surveys(code=code, first=True)
        return survey
    except Exception as e:
        mutils.raise_error('could not get first survey', e)
    return None


def pre_filter():
    return db.session.query(EndUserSurvey)


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
    for i in db_list:
        survey = i.ret_dict()
        em = json.loads(survey['result'])
        em['row_action'] = f"{i.id}"
        em['id'] = f"{i.id}"
        em['DT_RowId'] = f"{i.id}"
        out.append(em)
    return out

