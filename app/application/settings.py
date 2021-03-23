from app.data import settings as msettings
from app.application import utils as mutils


class StageSetting(msettings.StageSetting):
    pass


def get_configuration_settings():
    return msettings.get_configuration_settings()


def set_configuration_setting(setting, value):
    msettings.set_configuration_setting(setting, value)


def get_register_template():
    return msettings.get_configuration_setting('register-template')


def get_enable_enter_guest():
    return msettings.get_configuration_setting('enable-enter-guest')


def get_embedded_video_template():
    return msettings.get_configuration_setting('embedded-video-template')


def get_chat_room_template():
    return msettings.get_configuration_setting('chat-room-template')


def get_floating_video_template():
    return msettings.get_configuration_setting('floating-video-template')


def get_floating_pdf_template():
    return msettings.get_configuration_setting('floating-pdf-template')


def get_floating_document_template():
    return msettings.get_configuration_setting('floating-document-template')


def get_wonder_link_template():
    return msettings.get_configuration_setting('wonder-link-template')


def get_link_template():
    return msettings.get_configuration_setting('link-template')


def get_stage_delay(profile, stage):
    return msettings.get_configuration_setting(f'{profile}-stage-{stage}-delay')
