from app.data import utils as mutils, end_user as mend_user, visit as mvisit, floor as mfloor
import random, string, datetime
from app import log, flask_app
from app.application import socketio as msocketio, room as mroom, settings as msettings


def create_random_string(len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))


class Profile(mend_user.Profile):
    pass


class School(mend_user.School):
    pass


class Level(mend_user.Level):
    pass


def get_showtime(visit, stage):
    if visit.end_user.sub_profile == flask_app.config['ENTER_TEST_CODE']:
        visit.end_user.profile = 'Test'
        visit.timeslot = datetime.datetime.now()
    if visit.end_user.sub_profile == flask_app.config['DRY_RUN']:
        visit.timeslot = datetime.datetime.now()

    delay = msettings.get_stage_delay(visit.end_user.profile, stage)
    showtime = visit.timeslot + datetime.timedelta(seconds=delay)

    if visit.end_user.sub_profile == flask_app.config['ENTER_TEST_CODE']:
        visit.end_user.profile = Profile.E_GUEST

    log.info(f'user {visit.end_user.full_name()} stage {stage}, show time at {showtime}')
    return showtime


old_to_new_profile = {
    'guest': mend_user.Profile.E_GUEST,
    'floor-coworker': mend_user.Profile.E_FLOOR_COWORKER,
    'fair-coworker': mend_user.Profile.E_FAIR_COWORKER
}

def change_profile():
    user = mend_user.get_first_end_user(profile='guest')
    if user:
        users = mend_user.get_end_users()
        for user in users:
            if not user.profile in old_to_new_profile: continue
            new_profile = old_to_new_profile[user.profile]
            mend_user.update_end_user(user, profile=new_profile)

# The profile was saved in the database as an English term, but is displayed as a Dutch term, i.e. it was not
# possible to search for the profile in the database
change_profile()