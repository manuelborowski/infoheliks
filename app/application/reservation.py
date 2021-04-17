from app import db, log, flask_app
from app.data import settings as msettings, end_user as mend_user
from app.application import utils as mutils
import datetime, random, string, json


def create_random_string(len=32):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))


def add_end_user(first_name, last_name, email, profile):
    try:
        code = create_random_string()
        user = mend_user.get_first_end_user(email, profile)
        if user:
            log.info(f'add end user: {first_name} {last_name} {email} {profile} {code}: user already exists')
            return user
        user = mend_user.add_end_user(first_name, last_name, email, profile, code)
        log.info(f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: new user')
        return user
    except Exception as e:
        mutils.raise_error('could not add end user', e)
    return None


class RegisterSaveResult:
    def __init__(self, result, registration={}):
        self.result = result
        self.registration = registration

    class Result:
        E_OK = 'ok'
        E_REGISTER_OK = 'guest-ok'
        E_COULD_NOT_REGISTER = 'could-not-register'
        E_NOT_OPENED_YET = 'not-opened-yet'

    result = Result.E_OK
    registration = {}


def delete_registration(code=None, user_id_list=None):
    try:
        if code is not None:
            user = mend_user.get_first_end_user(code=code)
            user_id_list = [user.id]
        if user_id_list is not None:
            mend_user.delete_end_user(id_list=user_id_list)
    except Exception as e:
        mutils.raise_error(f'could not delete registration', e)


def add_registration(data, update_by_end_user=True):
    try:
        user = add_end_user(data['end-user-first-name'], data['end-user-last-name'], data['end-user-email'], data['end-user-profile'])
        if user:
            user.set_email_send_retry(0)
            if update_by_end_user:
                user.set_email_sent(False)
            return RegisterSaveResult(result=RegisterSaveResult.Result.E_REGISTER_OK, registration=user.flat())
        return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)
    except Exception as e:
        log.error(f'could not register: {e}')
        mutils.raise_error('could not add', e)
    return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)


def get_registration_template(code=None):
    try:
        if code == flask_app.config['REGISTER_GUEST_CODE']:
            register_template = json.loads(msettings.get_configuration_setting('register-guest-template'))
        elif code == flask_app.config['REGISTER_COWORKER_CODE']:
            register_template = json.loads(msettings.get_configuration_setting('register-coworker-template'))
        else:
            return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)
        ret = {'template': register_template}
        return RegisterSaveResult(result=RegisterSaveResult.Result.E_OK, registration=ret)
    except Exception as e:
        mutils.raise_error(f'could not get reservation by code {code}', e)
    return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)


def update_end_user_email_sent_by_id(id, value):
    try:
        return mend_user.update_email_sent_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id}, {value}', e)
    return None


def update_end_user_survey_email_sent_by_id(id, value):
    try:
        return mend_user.update_survey_email_sent_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id}, {value}', e)
    return None


def update_end_user_enable_by_id(id, value):
    try:
        return mend_user.update_enable_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit enable {id}, {value}', e)
    return None


def update_email_send_retry_by_id(id, value):
    try:
        return mend_user.update_email_send_retry_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update registration email-send-retry {id}, {value}', e)
    return None


def subscribe_end_user_ack_email_sent(cb, opaque):
    return mend_user.subscribe_ack_email_sent(cb, opaque)


def subscribe_end_user_survey_email_sent(cb, opaque):
    return mend_user.subscribe_survey_email_sent(cb, opaque)


def subscribe_end_user_email_send_retry(cb, opaque):
    return mend_user.subscribe_email_send_retry(cb, opaque)


def subscribe_visit_enabled(cb, opaque):
    return mend_user.subscribe_enabled(cb, opaque)


def add_test_user(code):
    user = mend_user.get_first_end_user(code=code)
    if not user:
        user = mend_user.add_end_user('test', code, 'emmanuel.borowski@gmail.com', mend_user.Profile.E_GUEST, code)


# add_test_user(flask_app.config['ENTER_TEST_CODE'])
# add_test_user(flask_app.config['DRY_RUN'])