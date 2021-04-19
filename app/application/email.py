from app.data import settings as msettings, end_user as mend_user
from app import email, log, email_scheduler, flask_app
import datetime, time, re
from flask_mail import Message


def send_email(to, subject, content):
    msg = Message(sender=flask_app.config['MAIL_USERNAME'], recipients=[to], subject=subject, html=content)
    try:
        email.send(msg)
        log.info(f'email sent to {to}')
        return True
    except Exception as e:
        log.error(f'send_email: ERROR, could not send email: {e}')
    return False


# def return_table_row(name, value):
def return_table_row(*cell_values):
    row_string = '<tr>'
    for value in cell_values:
        row_string += f'<td style="border:1px solid black;">{value}</td>'
    row_string += '</tr>'
    return row_string


def send_register_ack(**kwargs):
    try:
        user = mend_user.get_first_not_sent_registration()
        if user:
            email_send_max_retries = msettings.get_configuration_setting('email-send-max-retries')
            if user.email_send_retry >= email_send_max_retries:
                user.set_enabled(False)
                return
            user.set_email_send_retry(user.email_send_retry + 1)
            email_subject = msettings.get_configuration_setting('register-guest-mail-ack-subject-template')
            email_content = msettings.get_configuration_setting('register-guest-mail-ack-content-template')

            base_url = msettings.get_configuration_setting("base-url")
            enter_url = f'{base_url}/enter?code={user.code}'
            update_url = f'{base_url}/register?code={user.code}'

            email_content = email_content.replace('{{TAG-ENTER-URL}}', f'<a href="{enter_url}">deze link</a>')
            email_content = email_content.replace('{{TAG-UPDATE-URL}}', f'<a href="{update_url}">hier</a>')

            log.info(f'"{email_subject}" to {user.email}')
            ret = send_email(user.email, email_subject, email_content)
            if ret:
                user.set_email_sent(True)
            return ret
        return False
    except Exception as e:
        log.error(f'Could not send e-mail {e}')
    return False


send_email_config = [
    {'function': send_register_ack, 'args': {}},
]


def subscribe_send_email(cb, args):
    if cb:
        send_email_config.append({
            'function': cb,
            'args': args
        })


run_email_task = True
def send_email_task():
    nbr_sent_per_minute = 0
    while run_email_task:
        with flask_app.app_context():
            at_least_one_email_sent = True
            start_time = datetime.datetime.now()
            job_interval = msettings.get_configuration_setting('email-task-interval')
            emails_per_minute = msettings.get_configuration_setting('emails-per-minute')
            while at_least_one_email_sent:
                at_least_one_email_sent = False
                for send_email in send_email_config:
                    if run_email_task and msettings.get_configuration_setting('enable-send-email'):
                        ret = send_email['function'](**send_email['args'])
                        if ret:
                            nbr_sent_per_minute += 1
                            now = datetime.datetime.now()
                            delta = now - start_time
                            if (nbr_sent_per_minute >= emails_per_minute) and (delta < datetime.timedelta(seconds=60)):
                                time_to_wait = 60 - delta.seconds + 1
                                log.info(f'send_email_task: have to wait for {time_to_wait} seconds')
                                time.sleep(time_to_wait)
                                nbr_sent_per_minute = 0
                                start_time = datetime.datetime.now()
                            at_least_one_email_sent = True
        if run_email_task:
                now = datetime.datetime.now()
                delta = now - start_time
                if delta < datetime.timedelta(seconds=job_interval):
                    time_to_wait = job_interval - delta.seconds
                    time.sleep(time_to_wait)


def set_base_url(url):
    msettings.set_configuration_setting('base-url', url)


def stop_send_email_task():
    global run_email_task
    run_email_task = False


def start_send_email_task():
    running_job = email_scheduler.get_job('send_email_task')
    if running_job:
        email_scheduler.remove_job('send_email_task')
    email_scheduler.add_job('send_email_task', send_email_task)

start_send_email_task()

