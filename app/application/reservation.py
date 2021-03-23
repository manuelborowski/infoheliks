from app import db, log, flask_app
from app.data import reservation as mreservation, meeting as mmeeting, settings as msettings, visit as mvisit, \
    end_user as mend_user, floor as mfloor, fair as mfair, room as mroom, info_items as minfo_items
from app.application import utils as mutils
import datetime, random, string, json


def add_or_update_end_user_and_visit(first_name, last_name, email, profile, sub_profile, timeslot, code=None):
    try:
        if code:  # update of existing visit
            visit = mvisit.get_first_visit(code=code)
            user = visit.end_user
            mvisit.update_visit(visit, timeslot=timeslot)
            mend_user.update_end_user(user, first_name=first_name, last_name=last_name, email=email, profile=profile,
                                      sub_profile=sub_profile)
        else:
            code = create_random_string()
            user = mend_user.get_first_end_user(email, profile, sub_profile)
            if profile == mend_user.Profile.E_GUEST:
                if user:  # guest already present
                    mend_user.update_end_user(user, first_name=first_name, last_name=last_name)
                    visit = mvisit.get_first_visit(user=user, timeslot=timeslot)
                    if not visit:  # guest has this timeslot not yet
                        visit = mvisit.add_visit(timeslot, code)
                        user.add_visit(visit)
                        log.info(
                            f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: new timeslot')
                    else:
                        log.info(
                            f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: existing timeslot')
                else:  # new guest
                    user = mend_user.add_end_user(first_name, last_name, email, profile, sub_profile)
                    visit = mvisit.add_visit(timeslot, code)
                    user.add_visit(visit)
                    log.info(f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: new user')
            else:
                if user:  # coworker already present
                    mend_user.update_end_user(user, first_name=first_name, last_name=last_name)
                    visit = mvisit.get_first_visit(user=user)
                    log.info(
                        f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: user already exists')
                else:  # new coworker
                    user = mend_user.add_end_user(first_name, last_name, email, profile, sub_profile)
                    visit = mvisit.add_visit(timeslot, code)
                    user.add_visit(visit)
                    if user.profile == mend_user.Profile.E_FLOOR_COWORKER:
                        floor = mfloor.get_first_floor(level=user.sub_profile)
                        if floor.has_chat:
                            add_or_update_room(visit)
                    log.info(f'add end user: {first_name} {last_name} {email} {code} {profile} {code}: new user')
        return visit
    except Exception as e:
        mutils.raise_error('could not add end user/visit', e)
    return None


def add_or_update_room(visit):
    room = mroom.get_first_room(visit.code)
    if not room:
        room = mroom.add_room(visit.code, visit.end_user.sub_profile, visit.end_user.full_name())
    return room


def add_available_period(period, period_length, max_nbr_boxes):
    return mreservation.add_available_period(period, period_length, max_nbr_boxes)


def get_available_timeslots():
    available_timeslots = []
    try:
        first_timeslot = msettings.get_configuration_setting('timeslot-first-start')
        nbr_timeslots = msettings.get_configuration_setting('timeslot-number')
        timeslot_length = msettings.get_configuration_setting('timeslot-length')
        nbr_guests_per_timeslot = msettings.get_configuration_setting('timeslot-max-guests')
        first_break_timeslot = msettings.get_configuration_setting('timeslot-break-first-start')
        nbr_break_timeslots = msettings.get_configuration_setting('timeslot-break-number')
        last_break_timeslot = first_break_timeslot + datetime.timedelta(minutes=timeslot_length * (nbr_break_timeslots - 1))
        for i in range(nbr_timeslots):
            timeslot = first_timeslot + datetime.timedelta(minutes=timeslot_length * i)
            max_guests = 0 if timeslot >= first_break_timeslot and timeslot <= last_break_timeslot else nbr_guests_per_timeslot
            visits = mvisit.get_visits(timeslot=timeslot)
            nbr_guests_on_site = mvisit.get_visits(timeslot=timeslot, count=True, room_code_present=True)
            nbr_guests_in_wonder = mvisit.get_visits(timeslot=timeslot, count=True, survey_email_send_retry=1)
            nbr_visits = len(visits)
            available_timeslots.append({
                'label': mutils.datetime_to_dutch_datetime_string(timeslot),
                'timeslot': timeslot,
                'value': i,
                'max_visits': max_guests,
                'nbr_visits': nbr_visits,
                'nbr_visits_available': max_guests - nbr_visits,
                'nbr_visits_on_site': nbr_guests_on_site,
                'nbr_visits_in_wonder': nbr_guests_in_wonder,
            })
        return available_timeslots
    except Exception as e:
        mutils.raise_error('could not get available timeslots', e)
    return []


def format_timeslot_data():
    out = []
    timeslots = get_available_timeslots()
    for i, timeslot in enumerate(timeslots):
        out.append({
            'row_action': i+1,
            'timeslot': timeslot['label'],
            'nbr_visits': timeslot['nbr_visits'],
            'max_visits': timeslot['max_visits'],
            'nbr_on_site': timeslot['nbr_visits_on_site'],
            'nbr_in_wonder': timeslot['nbr_visits_in_wonder'],
        })
    return out


def get_available_floors():
    floors = mfloor.get_floors()
    return [{'label': f.level, 'value': f.id} for f in floors]


def get_available_fairs():
    fairs = mfair.get_fairs()
    return [{'label': f.school, 'value': f.id} for f in fairs]


def get_visits_available_for_timeslot(index):
    try:
        first_timeslot = msettings.get_configuration_setting('timeslot-first-start')
        nbr_timeslots = msettings.get_configuration_setting('timeslot-number')
        timeslot_length = msettings.get_configuration_setting('timeslot-length')
        nbr_guests_per_timeslot = msettings.get_configuration_setting('timeslot-max-guests')
        if index >= nbr_timeslots:
            return -1
        timeslot = first_timeslot + datetime.timedelta(minutes=timeslot_length * index)
        visits = mvisit.get_visits(timeslot=timeslot)
        nbr_visits_available = nbr_guests_per_timeslot - len(visits)
        return nbr_visits_available
    except Exception as e:
        mutils.raise_error(f'could not get visits left for timeslot {index}', e)
    return -1


def get_date_for_timeslot(index):
    try:
        first_timeslot = msettings.get_configuration_setting('timeslot-first-start')
        nbr_timeslots = msettings.get_configuration_setting('timeslot-number')
        timeslot_length = msettings.get_configuration_setting('timeslot-length')
        if index >= nbr_timeslots:
            return None
        timeslot = first_timeslot + datetime.timedelta(minutes=timeslot_length * index)
        return timeslot
    except Exception as e:
        mutils.raise_error(f'could not get timeslot date: {index}', e)
    return None


def get_index_for_timeslot(date):
    try:
        first_timeslot = msettings.get_configuration_setting('timeslot-first-start')
        timeslot_length = msettings.get_configuration_setting('timeslot-length')
        delta_time_minutes = (date - first_timeslot) / datetime.timedelta(minutes=1)
        index = delta_time_minutes / timeslot_length
        return int(index)
    except Exception as e:
        mutils.raise_error(f'could not get timeslot index: {date}', e)
    return None


def get_id_for_floor(floor_string):
    try:
        floor = mfloor.get_first_floor(level=floor_string)
        return int(floor.id)
    except Exception as e:
        mutils.raise_error(f'could not get floor id: {floor_string}', e)
    return None


def get_id_for_fair(fair_string):
    try:
        fair = mfair.get_first_fair(school=fair_string)
        return int(fair.id)
    except Exception as e:
        mutils.raise_error(f'could not get fair id: {fair_string}', e)
    return None


def get_period_by_id(id):
    return mreservation.get_available_period_by_id(id)


def create_random_string(len=32):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))


class RegisterSaveResult:
    def __init__(self, result, registration={}):
        self.result = result
        self.registration = registration

    class Result:
        E_OK = 'ok'
        E_GUEST_OK = 'guest-ok'
        E_FLOOR_COWORKER_OK = 'floor-coworker-ok'
        E_FAIR_COWORKER_OK = 'fair-coworker-ok'
        E_NO_BOXES_SELECTED = 'no-boxes-selected'
        E_NOT_ENOUGH_BOXES = 'not-enough-boxes'
        E_COULD_NOT_REGISTER = 'could-not-register'
        E_NOT_ENOUGH_VISITS = 'not-enough-visits'
        E_NO_VISIT_SELECTED = 'no-visit-selected'
        E_NO_FLOOR_SELECTED = 'no-floor-selected'
        E_NO_FAIR_SELECTED = 'no-fair-selected'
        E_NO_REGISTRATION_FOUND = 'no-registration-found'
        E_NOT_OPENED_YET = 'not-opened-yet'

    result = Result.E_OK
    registration = {}


def delete_registration(code=None, visit_id_list=None):
    try:
        if code is not None:
            visit = mvisit.get_first_visit(code=code)
            visit_id_list = [visit.id]
        if visit_id_list is not None:
            for id in visit_id_list:
                visit = mvisit.get_first_visit(id=id)
                user = mend_user.get_first_end_user(code=visit.code)
                rooms = mroom.get_rooms(code=visit.code)
                mvisit.delete_visit(id=id)
                if not user.visits:
                    mend_user.delete_end_user(user=user)
                    for room in rooms:
                        mroom.delete_room(room)
    except Exception as e:
        mutils.raise_error(f'could not delete registration', e)


def add_or_update_registration(data, update_by_end_user=True):
    try:
        registration_code = data['registration-code'] if data['registration-code'] != '' else None
        if data['end-user-profile'] == mend_user.Profile.E_GUEST:
            reservation_info = {'code': flask_app.config['REGISTER_GUEST_CODE']}
            if 'radio-visit-timeslots' not in data or data['radio-visit-timeslots'] == '':
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_NO_VISIT_SELECTED,
                                          registration=reservation_info)
            nbr_visits_available = get_visits_available_for_timeslot(data['radio-visit-timeslots'])
            timeslot = get_date_for_timeslot(data['radio-visit-timeslots'])
            if nbr_visits_available <= 0:
                reservation_info.update({'timeslot': mutils.datetime_to_string(timeslot)})
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_NOT_ENOUGH_VISITS,
                                          registration=reservation_info)
            visit = add_or_update_end_user_and_visit(data['end-user-first-name'], data['end-user-last-name'],
                                                           data['end-user-email'], mend_user.Profile.E_GUEST, None,
                                                           timeslot, registration_code)
            if visit:
                visit.set_email_send_retry(0)
                if update_by_end_user:
                    visit.set_email_sent(False)
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_GUEST_OK, registration=visit.flat())
            return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)
        elif data['end-user-profile'] == mend_user.Profile.E_FLOOR_COWORKER:
            reservation_info = {'code': flask_app.config['REGISTER_FLOOR_COWORKER_CODE']}
            if 'radio-floor-levels' not in data or data['radio-floor-levels'] == '':
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_NO_FLOOR_SELECTED,
                                          registration=reservation_info)
            floor = mfloor.get_first_floor(id=data['radio-floor-levels'])
            timeslot = datetime.datetime.now()
            visit = add_or_update_end_user_and_visit(data['end-user-first-name'], data['end-user-last-name'],
                                                           data['end-user-email'], mend_user.Profile.E_FLOOR_COWORKER,
                                                           floor.level, timeslot, registration_code)
            if visit:
                # add_or_update_room(visit)
                visit.set_email_send_retry(0)
                if update_by_end_user:
                    visit.set_email_sent(False)
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_FLOOR_COWORKER_OK,
                                          registration=visit.flat())
            return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)
        elif data['end-user-profile'] == mend_user.Profile.E_FAIR_COWORKER:
            reservation_info = {'code': flask_app.config['REGISTER_FAIR_COWORKER_CODE']}
            if 'radio-fair-schools' not in data or data['radio-fair-schools'] == '':
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_NO_FAIR_SELECTED,
                                          registration=reservation_info)
            fair = mfair.get_first_fair(id=data['radio-fair-schools'])
            timeslot = datetime.datetime.now()
            visit = add_or_update_end_user_and_visit(data['end-user-first-name'], data['end-user-last-name'],
                                                           data['end-user-email'], mend_user.Profile.E_FAIR_COWORKER,
                                                           fair.school, timeslot, registration_code)
            if visit:
                visit.set_email_send_retry(0)
                if update_by_end_user:
                    visit.set_email_sent(False)
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_FAIR_COWORKER_OK,
                                          registration=visit.flat())
            return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)
    except Exception as e:
        log.error(f'could not register: {e}')
        mutils.raise_error('could not add or update registration', e)
    return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)


def get_default_values(code=None, id=None):
    try:
        register_endpoint = {'code': flask_app.config['REGISTER_GUEST_CODE']}
        visit = None
        profile = None
        if code:
            if code == flask_app.config['REGISTER_GUEST_CODE']:
                profile = mend_user.Profile.E_GUEST
            elif code == flask_app.config['REGISTER_FLOOR_COWORKER_CODE']:
                profile = mend_user.Profile.E_FLOOR_COWORKER
            elif code == flask_app.config['REGISTER_FAIR_COWORKER_CODE']:
                profile = mend_user.Profile.E_FAIR_COWORKER
            else:
                visit = mvisit.get_first_visit(code=code)
        elif id:
            visit = mvisit.get_first_visit(id=id)
        if visit:
            profile = visit.end_user.profile
        if profile:
            if profile == mend_user.Profile.E_GUEST:
                register_template = json.loads(msettings.get_configuration_setting('register-guest-template'))
                timeslots = get_available_timeslots()
                if visit:
                    default_settings = visit.flat()
                    default_settings.update({'radio-visit-timeslots': get_index_for_timeslot(visit.timeslot)})
                else:
                    default_settings = {'end-user-profile': mend_user.Profile.E_GUEST}
                ret = {'template': register_template,
                       'default': default_settings,
                       'timeslots': timeslots,
                       }
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_OK, registration=ret)
            elif profile == mend_user.Profile.E_FLOOR_COWORKER:
                register_template = json.loads(msettings.get_configuration_setting('register-floor-coworker-template'))
                floors = get_available_floors()
                if visit:
                    default_settings = visit.flat()
                    default_settings.update({'radio-floor-levels': get_id_for_floor(visit.end_user.sub_profile)})
                else:
                    default_settings = {'end-user-profile': mend_user.Profile.E_FLOOR_COWORKER}
                ret = {'template': register_template,
                       'default': default_settings,
                       'floors': floors
                       }
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_OK, registration=ret)
            elif profile == mend_user.Profile.E_FAIR_COWORKER:
                register_template = json.loads(msettings.get_configuration_setting('register-fair-coworker-template'))
                fairs = get_available_fairs()
                if visit:
                    default_settings = visit.flat()
                    default_settings.update({'radio-fair-schools': get_id_for_fair(visit.end_user.sub_profile)})
                else:
                    default_settings = {'end-user-profile': mend_user.Profile.E_FAIR_COWORKER}
                ret = {'template': register_template,
                       'default': default_settings,
                       'fairs': fairs
                       }
                return RegisterSaveResult(result=RegisterSaveResult.Result.E_OK, registration=ret)
        return RegisterSaveResult(result=RegisterSaveResult.Result.E_NO_REGISTRATION_FOUND,
                                  registration=register_endpoint)
    except Exception as e:
        mutils.raise_error(f'could not get reservation by code {code}', e)
    return RegisterSaveResult(result=RegisterSaveResult.Result.E_COULD_NOT_REGISTER)


def get_reservation_by_id(id):
    return mreservation.get_registration_by_id(id)


def delete_meeting(id=None, list=None):
    return mmeeting.delete_meeting(id, list)


def update_meeting_code_by_id(id, value):
    try:
        return mmeeting.update_meeting_code_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update meeting code {id}, {value}', e)
    return None


def update_meeting_email_sent_by_id(id, value):
    try:
        return mmeeting.update_meeting_email_sent_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update meeting email-sent {id}, {value}', e)
    return None


def update_meeting_email_enable_by_id(id, value):
    try:
        return mmeeting.update_meeting_email_enable_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update meeting enable email {id}, {value}', e)
    return None


def update_visit_email_sent_by_id(id, value):
    try:
        return mvisit.update_email_sent_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id}, {value}', e)
    return None


def update_visit_survey_email_sent_by_id(id, value):
    try:
        return mvisit.update_survey_email_sent_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit email-sent {id}, {value}', e)
    return None


def update_visit_enable_by_id(id, value):
    try:
        return mvisit.update_enable_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update visit enable {id}, {value}', e)
    return None


def update_email_send_retry_by_id(id, value):
    try:
        return mvisit.update_email_send_retry_by_id(id, value)
    except Exception as e:
        mutils.raise_error(f'could not update registration email-send-retry {id}, {value}', e)
    return None


def subscribe_meeting_ack_email_sent(cb, opaque):
    return mmeeting.subscribe_ack_email_sent(cb, opaque)


def subscribe_visit_ack_email_sent(cb, opaque):
    return mvisit.subscribe_ack_email_sent(cb, opaque)


def subscribe_visit_survey_email_sent(cb, opaque):
    return mvisit.subscribe_survey_email_sent(cb, opaque)


def subscribe_visit_email_send_retry(cb, opaque):
    return mvisit.subscribe_email_send_retry(cb, opaque)


def subscribe_visit_enabled(cb, opaque):
    return mvisit.subscribe_enabled(cb, opaque)


def add_test_user(code):
    visit = mvisit.get_first_visit(code=code)
    if not visit:
        visit = add_or_update_end_user_and_visit('test', code, 'emmanuel.borowski@gmail.com',
                                                 mend_user.Profile.E_GUEST, code, datetime.datetime.now())
        mvisit.update_visit(visit, code=code)


add_test_user(flask_app.config['ENTER_TEST_CODE'])
add_test_user(flask_app.config['DRY_RUN'])