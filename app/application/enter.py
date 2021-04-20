from app import flask_app
from app.application import reservation as mreservation, socketio as msocketio
from app.data import settings as msettings, utils as mutils, end_user as mend_user
from app.data.end_user import Profile
import json, datetime


class EnterResult:
    def __init__(self, result, ret={}):
        self.result = result
        self.ret = ret

    class Result:
        E_OK = 'ok'
        E_NOT_OPENED_YET = 'not-opened-yet'

    result = Result.E_OK
    ret = {}


def end_user_wants_to_enter(code=None):
    is_opened = msettings.get_configuration_setting('enable-enter-guest')
    user = mend_user.get_first_end_user(code=code)
    if user:
        if user.profile == Profile.E_GUEST:
            now = datetime.datetime.now()
            site_open = msettings.get_configuration_setting('site-open-at')
            delta = (site_open - now).total_seconds()
            if delta > 60 or not is_opened:
                return EnterResult(result=EnterResult.Result.E_NOT_OPENED_YET)
        user.set_timestamp()
        ret = {
            'template': json.loads(msettings.get_configuration_setting('infosession-template')),
            'user': user.flat(),
            'content': json.loads(msettings.get_configuration_setting('infosession-content-json'))
            }
        return EnterResult(result=EnterResult.Result.E_OK, ret=ret)
    return EnterResult(result=EnterResult.Result.E_NOT_OPENED_YET)


def get_wonder_links():
    try:
        link = msettings.get_configuration_setting('wonder-link')
        return [link]
    except Exception as e:
        mutils.raise_error(f'could not get wonder link', e)


def user_enters_wonder_room(msg, sid):
    code = msg['data']['code']
    # visit = mvisit.get_first_visit(code=code)
    # mvisit.update_visit(visit, survey_email_send_retry=1)


msocketio.subscribe_on_type('enter-wonder-room', user_enters_wonder_room)