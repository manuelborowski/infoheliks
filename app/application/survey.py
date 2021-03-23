from app import log
from app.data import settings as msettings, visit as mvisit, survey as msurvey, end_user as mend_user
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
        visit = mvisit.get_first_visit(code=code)
        if visit:
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
        visit = mvisit.get_first_visit(code=code)
        if visit:
            template = json.loads(msettings.get_configuration_setting('survey-default-results-template'))
            template = mutils.deepupdate(template, data)
            data_string = json.dumps(template).replace('true', '1').replace('false', '0')
            survey = msurvey.get_first_survey(code=code)
            if survey:
                msurvey.update_survey(survey, data=data_string)
            else:
                msurvey.add_survey(code, data_string)
            return SurveyResult(result=SurveyResult.Result.E_OK)
    except Exception as e:
        mutils.raise_error(f'could not add survey', e)
    return SurveyResult(result=SurveyResult.Result.E_NO_VALID_CODE)


def send_survey_email(**kwargs):
    try:
        visit = mvisit.get_first_not_sent_survey()
        if visit:
            email_send_max_retries = msettings.get_configuration_setting('email-send-max-retries')
            if visit.email_send_retry >= email_send_max_retries:
                visit.set_enabled(False)
                return
            visit.set_email_send_retry(visit.email_send_retry + 1)
            email_subject = msettings.get_configuration_setting('survey-mail-subject-template')
            email_content = msettings.get_configuration_setting('survey-mail-content-template')
            base_url = msettings.get_configuration_setting("base-url")
            survey_url = f'{base_url}/survey_new?code={visit.code}'

            email_content = email_content.replace('{{URL-TAG}}', f'<a href="{survey_url}">hier</a>')
            log.info(f'"{email_subject}" to {visit.end_user.email}')
            ret = memail.send_email(visit.end_user.email, email_subject, email_content)
            if ret:
                visit.set_survey_email_sent(True)
            return ret
        return False
    except Exception as e:
        log.error(f'Could not send e-mail {e}')
    return False


memail.subscribe_send_email(send_survey_email, {})

true = True
false = False

survey_default_results = \
    {
        "city": "",
        "school": "",
        "information-channel": {
            "broodzak": false,
            "infoborden": false,
            "school": false,
            "andere": false
        },
        "stage-2-score": {
            "intro-movie": "",
            "clb-info": "",
            "scholengemeenschap-info": "",
            "internaat-info": "",
            "chat-info": ""
        },
        "stage-2-feedback": "",
        "stage-3-score": {
            "able-to-ask-questions": "",
            "video-chat-experience": ""
        },
        "stage-3-feedback": "",
        "guest-code": "",
        "submit": false,
        "information-channel-other": "",
    }
