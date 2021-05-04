from app import log
from app.data import settings as msettings, survey as msurvey, end_user as mend_user
from app.application import email as memail, utils as mutils
import json


class SurveyResult:
    def __init__(self, result, ret={}):
        self.result = result
        self.ret = ret

    class Result:
        E_OK = 'ok'
        E_NO_VALID_CODE = 'no-valid-code'

    result = Result.E_OK
    ret = {}


def get_survey_template(code=None):
    try:
        user = mend_user.get_first_end_user(code=code)
        if user:
            template = json.loads(msettings.get_configuration_setting('survey-template'))
            ret = {
                'template': template,
                'default_values': {
                    'guest-code': code,
                },
            }
            return SurveyResult(result=SurveyResult.Result.E_OK, ret=ret)
    except Exception as e:
        mutils.raise_error(f'could not get survey template for {code}', e)
    return SurveyResult(result=SurveyResult.Result.E_NO_VALID_CODE)


def save_survey(data):
    try:
        code = data['guest-code']
        user = mend_user.get_first_end_user(code=code)
        survey = msurvey.get_first_survey(code=code)
        template = json.loads(msettings.get_configuration_setting('survey-default-results-template'))
        template = mutils.deepupdate(template, data)
        data_string = json.dumps(template).replace('true', '1').replace('false', '0')
        if survey:
            msurvey.update_survey(survey=survey, data=data_string)
        else:
            msurvey.add_survey(code=code, data=data_string)
        return SurveyResult(result=SurveyResult.Result.E_OK)
    except Exception as e:
        mutils.raise_error(f'could not add survey', e)
    return SurveyResult(result=SurveyResult.Result.E_NO_VALID_CODE)


def send_survey_email(**kwargs):
    try:
        if not msettings.get_configuration_setting('enable-send-survey-email'):
            return
        user = mend_user.get_first_not_sent_survey()
        if user:
            email_send_max_retries = msettings.get_configuration_setting('email-send-max-retries')
            if user.email_send_retry >= email_send_max_retries:
                user.set_enabled(False)
                return
            user.set_email_send_retry(user.email_send_retry + 1)
            email_subject = msettings.get_configuration_setting('survey-mail-subject-template')
            email_content = msettings.get_configuration_setting('survey-mail-content-template')
            base_url = msettings.get_configuration_setting("base-url")
            survey_url = f'{base_url}/survey_new?code={user.code}'

            email_content = email_content.replace('{{URL-TAG}}', f'<a href="{survey_url}">hier</a>')
            log.info(f'"{email_subject}" to {user.email}')
            ret = memail.send_email(user.email, email_subject, email_content)
            if ret:
                user.set_survey_email_sent(True)
            return ret
        return False
    except Exception as e:
        log.error(f'Could not send e-mail {e}')
    return False


memail.subscribe_send_email(send_survey_email, {})
