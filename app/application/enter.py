from app import flask_app
from app.application import room as mroom, end_user as mend_user, reservation as mreservation, socketio as msocketio
from app.data import settings as msettings, visit as mvisit, info_items as minfo_items, utils as mutils
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
    visit = mvisit.get_first_visit(code=code)
    if visit.end_user.profile == Profile.E_GUEST:
        now = datetime.datetime.now()
        delta = (visit.timeslot - now).total_seconds()
        if delta > 60:
            return EnterResult(result=EnterResult.Result.E_NOT_OPENED_YET)

    if is_opened or \
            visit.end_user.sub_profile == flask_app.config['ENTER_TEST_CODE'] or \
            visit.end_user.sub_profile == flask_app.config['DRY_RUN'] or \
            visit.end_user.profile != Profile.E_GUEST:
        template = json.loads(msettings.get_configuration_setting('infosession-template'))
        popup = msettings.get_configuration_setting('enter-site-popup-template')

        visit.set_timestamp()
        ret = {
            'template': template,
            'default_values': {
                'enter_site_popup': popup,
                'chat_history': mroom.get_chat_rooms_history(),
                'stage_2_showtime': str(mend_user.get_showtime(visit, 2)),
                'stage_3_showtime': str(mend_user.get_showtime(visit, 3)),
                'stage_4_showtime': str(mend_user.get_showtime(visit, 4)),
            },
            'user': visit.flat(),
            'tabpages': json.loads(msettings.get_configuration_setting('infosession-content-json'))
        }
        return EnterResult(result=EnterResult.Result.E_OK, ret=ret)
    return EnterResult(result=EnterResult.Result.E_NOT_OPENED_YET)


def get_wonder_links(flat_user):
    try:
        visit = mvisit.get_first_visit(code=flat_user['code'])
        if visit.end_user.profile == Profile.E_GUEST:
            even_timeslot = round(visit.timeslot.minute / 10) % 2 == 0
            if even_timeslot:
                link = msettings.get_configuration_setting('wonder-link-even')
            else:
                link = msettings.get_configuration_setting('wonder-link-odd')
            return [{
                    'timeslot': flat_user['timeslot'],
                    'link': link
                }]
        test_wonder_room = msettings.get_configuration_setting('test-wonder-room')
        links = []
        if test_wonder_room:
            links.append({
                'timeslot': '14.00 (Generale repetitie wonderkamer)',
                'link': msettings.get_configuration_setting('wonder-link-even')
            })
            pass
        else:
            timeslots = mreservation.get_available_timeslots()
            for timeslot in timeslots:
                if timeslot['max_visits'] == 0: continue
                even_timeslot = round(timeslot['timeslot'].minute / 10) % 2 == 0
                if even_timeslot:
                    link = msettings.get_configuration_setting('wonder-link-even')
                else:
                    link = msettings.get_configuration_setting('wonder-link-odd')
                links.append({
                        'timeslot': timeslot['label'],
                        'link': link
                    })
        return links
    except Exception as e:
        mutils.raise_error(f'could not get wonder links', e)


def user_enters_wonder_room(msg, sid):
    code = msg['data']['code']
    visit = mvisit.get_first_visit(code=code)
    mvisit.update_visit(visit, survey_email_send_retry=1)


msocketio.subscribe_on_type('enter-wonder-room', user_enters_wonder_room)