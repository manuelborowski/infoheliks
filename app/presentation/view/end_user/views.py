from flask import render_template, request
from . import end_user
from app import log, socketio
from app.application import reservation as mreservation, email as memail, enter as menter, survey as msurvey
import json, re
from app.presentation.view import  prepare_registration_form, prepare_enter_form


@end_user.route('/register', methods=['POST', 'GET'])
def register():
    try:

        current_url = request.url
        current_url = re.sub(f'{request.url_rule.rule}.*', '', current_url)
        memail.set_base_url(current_url)
        code = request.args['code']
        ret = prepare_registration_form(code=code)
        if ret.result == ret.Result.E_COULD_NOT_REGISTER:
            return render_template('end_user/messages.html', type='could-not-register')
        if ret.result == ret.Result.E_NO_REGISTRATION_FOUND:
            return render_template('end_user/messages.html', type='no-registration-found', info=ret.registration)
        return render_template('end_user/register.html', config_data=ret.registration,
                               registration_endpoint = 'end_user.register_save')
    except Exception as e:
        log.error(f'could not register {request.args}: {e}')
        return render_template('end_user/messages.html', type='unknown-error', message=e)


@end_user.route('/register_save/<string:form_data>', methods=['POST', 'GET'])
def register_save(form_data):
    try:
        data = json.loads(form_data)
        if data['cancel-reservation']:
            try:
                mreservation.delete_registration(code=data['registration-code'])
                return render_template('end_user/messages.html', type='cancel-ok')
            except Exception as e:
                return render_template('end_user/messages.html', type='could-not-cancel', message=e)
        else:
            try:
                ret = mreservation.add_or_update_registration(data)
                if ret.result == ret.Result.E_NO_VISIT_SELECTED:
                    return render_template('end_user/messages.html', type='no-visit-selected', info=ret.registration)
                if ret.result == ret.Result.E_NOT_ENOUGH_VISITS:
                    return render_template('end_user/messages.html', type='not-enough-visits', info=ret.registration)
                if ret.result == ret.Result.E_GUEST_OK:
                    return render_template('end_user/messages.html', type='register-guest-ok', info=ret.registration)

                if ret.result == ret.Result.E_NO_FLOOR_SELECTED:
                    return render_template('end_user/messages.html', type='no-floor-selected', info=ret.registration)
                if ret.result == ret.Result.E_FLOOR_COWORKER_OK:
                    return render_template('end_user/messages.html', type='register-floor-coworker-ok', info=ret.registration)

                if ret.result == ret.Result.E_NO_FAIR_SELECTED:
                    return render_template('end_user/messages.html', type='no-fair-selected', info=ret.registration)
                if ret.result == ret.Result.E_FAIR_COWORKER_OK:
                    return render_template('end_user/messages.html', type='register-fair-coworker-ok', info=ret.registration)

            except Exception as e:
                return render_template('end_user/messages.html', type='could-not-register', message=e)
            return render_template('end_user/messages.html', type='could-not-register')
    except Exception as e:
        return render_template('end_user/messages.html', type='unknown-error', message=e)


@end_user.route('/enter', methods=['POST', 'GET'])
def enter():
    try:
        code = request.args['code']
        ret = prepare_enter_form(code)
        if ret.result == ret.Result.E_NOT_OPENED_YET:
            return render_template('end_user/messages.html', type='not-opened-yet')
    except Exception as e:
        log.error(f'coworker with args {request.args} could not enter: {e}')
        return render_template('end_user/messages.html', type='could-not-enter')
    return render_template('end_user/infomoment.html', config_data=ret.ret,
                           async_mode=socketio.async_mode, template=ret.ret['template'])


@end_user.route('/survey_new', methods=['POST', 'GET'])
def survey():
    try:
        code = request.args['code']
        ret = msurvey.get_survey_template(code)
        if ret.result == ret.Result.E_OK:
            return render_template('end_user/survey.html',
                                   survey_endpoint='end_user.survey_save',
                                   async_mode=socketio.async_mode,
                                   template=ret.ret['template'],
                                   default_values=ret.ret['default_values']
                                   )
    except Exception as e:
        log.error(f'guest with args {request.args} could not enter survey: {e}')
    return render_template('end_user/messages.html', type='could-not-enter')


@end_user.route('/survey_save/<string:form_data>', methods=['POST', 'GET'])
def survey_save(form_data):
    try:
        data = json.loads(form_data)
        ret = msurvey.save_survey(data)
        if ret.result == ret.Result.E_OK:
            return render_template('end_user/messages.html', type='survey-ok')
    except Exception as e:
        log.error(f'could not add survey')
    return render_template('end_user/messages.html', type='unknown-error')


