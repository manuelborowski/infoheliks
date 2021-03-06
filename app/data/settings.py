from flask_login import current_user
from app.data.models import Settings
from app import log
from app import db
import datetime


# return: found, value
# found: if True, setting was found else not
# value ; if setting was found, returns the value
def get_setting(name, id=-1):
    try:
        setting = Settings.query.filter_by(name=name, user_id=id if id > -1 else current_user.id).first()
        if setting.type == Settings.SETTING_TYPE.E_INT:
            value = int(setting.value)
        elif setting.type == Settings.SETTING_TYPE.E_FLOAT:
            value = float(setting.value)
        elif setting.type == Settings.SETTING_TYPE.E_BOOL:
            value = setting.value == 'True'
        elif setting.type == Settings.SETTING_TYPE.E_DATETIME:
            value = datetime.datetime.strptime(setting.value, '%Y-%m-%d %H:%M:%S:%f')
        else:
            value = setting.value
    except:
        return False, ''
    return True, value


def add_setting(name, value, type, id=-1):
    setting = Settings(name=name, value='', type=type, user_id=id if id > -1 else current_user.id)
    db.session.add(setting)
    set_setting(name, value, id)
    log.info('add: {}'.format(setting.log()))
    return True


def set_setting(name, value, id=-1):
    try:
        setting = Settings.query.filter_by(name=name, user_id=id if id > -1 else current_user.id).first()
        if setting.type == Settings.SETTING_TYPE.E_DATETIME:
            setting.value = value.strftime('%Y-%m-%d %H:%M:%S:%f')
        else:
            setting.value = str(value)
        db.session.commit()
    except:
        return False
    return True


def get_test_server():
    found, value = get_setting('test_server', 1)
    if found: return value
    add_setting('test_server', False, Settings.SETTING_TYPE.E_BOOL, 1)
    return False


class StageSetting:
    E_AFTER_START_TIMESLOT = "start-timeslot"
    E_AFTER_LOGON = "logon"


# timeslots
# 14.00u – 14.30u – 15.00u - 15.30u - 16.00u – 19.00u –
# 19.30u – 20.00u – 20.30u

#spare timeslots
# 17.00 u - 17.30u - 18.00u - 18.30u

default_configuration_settings = {
    'register-guest-template': ('', Settings.SETTING_TYPE.E_STRING),
    'register-guest-mail-ack-subject-template': ('', Settings.SETTING_TYPE.E_STRING),
    'register-guest-mail-ack-content-template': ('', Settings.SETTING_TYPE.E_STRING),

    'register-coworker-template': ('', Settings.SETTING_TYPE.E_STRING),
    'register-coworker-mail-ack-subject-template': ('', Settings.SETTING_TYPE.E_STRING),
    'register-coworker-mail-ack-content-template': ('', Settings.SETTING_TYPE.E_STRING),

    'email-send-max-retries': (2, Settings.SETTING_TYPE.E_INT),
    'email-task-interval': (10, Settings.SETTING_TYPE.E_INT),
    'emails-per-minute': (30, Settings.SETTING_TYPE.E_INT),
    'base-url': ('localhost:5000', Settings.SETTING_TYPE.E_STRING),
    'enable-send-email': (False, Settings.SETTING_TYPE.E_BOOL),

    'enable-enter-guest': (False, Settings.SETTING_TYPE.E_BOOL),

    'infosession-template': ('', Settings.SETTING_TYPE.E_STRING),

    'embedded-video-template': ('', Settings.SETTING_TYPE.E_STRING),
    'floating-video-template': ('', Settings.SETTING_TYPE.E_STRING),
    'floating-pdf-template': ('', Settings.SETTING_TYPE.E_STRING),
    'floating-document-template': ('', Settings.SETTING_TYPE.E_STRING),
    'link-template': ('', Settings.SETTING_TYPE.E_STRING),
    'infosession-content-json': ('', Settings.SETTING_TYPE.E_STRING),

    'wonder-link': ('https://www.wonder.me/r?id=816ecec6-802e-468e-b9d5-7950f8f7f58a', Settings.SETTING_TYPE.E_STRING),

    'wonder-link-template': ('', Settings.SETTING_TYPE.E_STRING),

    'survey-template': ('', Settings.SETTING_TYPE.E_STRING),
    'survey-default-results-template': ('', Settings.SETTING_TYPE.E_STRING),
    'survey-mail-subject-template': ('', Settings.SETTING_TYPE.E_STRING),
    'survey-mail-content-template': ('', Settings.SETTING_TYPE.E_STRING),
    'enable-send-survey-email': (False, Settings.SETTING_TYPE.E_BOOL),

    'test-wonder-room': (True, Settings.SETTING_TYPE.E_BOOL),

    'enter-site-popup-template': ('', Settings.SETTING_TYPE.E_STRING),
    # 'site-open-at': ('2021-05-03 19:00', Settings.SETTING_TYPE.E_DATETIME),
    'site-open-at': (datetime.datetime(2021, 5, 3, 19, 00), Settings.SETTING_TYPE.E_DATETIME),
}


def get_configuration_settings():
    configuration_settings = {}
    for k in default_configuration_settings:
        configuration_settings[k] = get_configuration_setting(k)
    return configuration_settings


def set_configuration_setting(setting, value):
    if None == value:
        value = default_configuration_settings[setting][0]
    return set_setting(setting, value, 1)


def get_configuration_setting(setting):
    found, value = get_setting(setting, 1)
    if found:
        return value
    else:
        default_setting = default_configuration_settings[setting]
        add_setting(setting, default_setting[0], default_setting[1], 1)
        return default_setting[0]


# save settings which are not in the database yet
# get_configuration_settings()