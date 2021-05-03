from . import reservation
from app import admin_required, log, supervisor_required
from flask import redirect, url_for, request, render_template
from flask_login import login_required
from app.presentation.view import base_multiple_items
from app.data import end_user as mend_user
from app.application import reservation as mreservation, settings as msettings, socketio as msocketio
from app.data.models import EndUser
from app.presentation.layout.utils import flash_plus, button_pressed
from app.presentation.view import update_available_periods, false, true, null, prepare_registration_form

import json


@reservation.route('/reservation', methods=['POST', 'GET'])
@login_required
@supervisor_required
def show():
    return base_multiple_items.show(table_configuration)


@reservation.route('/reservation/table_ajax', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_ajax():
    return base_multiple_items.ajax(table_configuration)


@reservation.route('/reservation/table_action', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_action():
    pass
    if button_pressed('edit'):
        return item_edit()
    if button_pressed('delete'):
        return item_delete()


def item_edit(done=False, id=-1):
    try:
        chbx_id_list = request.form.getlist('chbx')
        if chbx_id_list:
            id = int(chbx_id_list[0])  # only the first one can be edited
        ret = prepare_registration_form(id=id)
        if ret.result == ret.Result.E_COULD_NOT_REGISTER:
            flash_plus('Fout opgetreden')
        if ret.result == ret.Result.E_NO_REGISTRATION_FOUND:
            flash_plus('Geen registratie gevonden')
        return render_template('end_user/register.html', config_data=ret.registration,
                               registration_endpoint = 'reservation.reservation_save')
    except Exception as e:
        log.error(f'could not edit reservation {request.args}: {e}')
        return redirect(url_for('reservation.show'))


def item_delete():
    try:
        chbx_id_list = request.form.getlist('chbx')
        mreservation.delete_registration(user_id_list=chbx_id_list)
    except Exception as e:
        log.error(f'Could not delete registration: {e}')
        flash_plus(u'Kan de registraties niet verwijderen', e)
    return redirect(url_for('reservation.show'))


@reservation.route('/reservation_save/<string:form_data>', methods=['POST', 'GET'])
@login_required
@supervisor_required
def reservation_save(form_data):
    try:
        data = json.loads(form_data)
        if data['cancel-reservation']:
            try:
                mreservation.delete_registration(code=data['registration-code'])
            except Exception as e:
                flash_plus('Kon de reservatie niet verwijderen', e)
        else:
            try:
                ret = mreservation.add_registration(data, update_by_end_user=False)
                if ret.result == ret.Result.E_NO_VISIT_SELECTED:
                    flash_plus('Geen tijdslot geselecteerd')
                if ret.result == ret.Result.E_NOT_ENOUGH_VISITS:
                    flash_plus('Niet genoeg tijdsloten')
            except Exception as e:
                flash_plus('Onbekende fout opgetreden', e)
    except Exception as e:
        flash_plus('Onbekende fout opgetreden', e)
    return redirect(url_for('reservation.show'))


def update_meeting_cb(msg, client_sid=None):
    if msg['data']['column'] == 5:  # registration ack mail sent column
        mreservation.update_end_user_email_sent_by_id(msg['data']['id'], msg['data']['value'])
    if msg['data']['column'] == 6:  # survey mail sent column
        mreservation.update_end_user_survey_email_sent_by_id(msg['data']['id'], msg['data']['value'])
    if msg['data']['column'] == 7:  # enable  column
        mreservation.update_end_user_enable_by_id(msg['data']['id'], msg['data']['value'])
    if msg['data']['column'] == 8:  # update tx-retry column
        mreservation.update_email_send_retry_by_id(msg['data']['id'], msg['data']['value'])
    msocketio.send_to_room({'type': 'celledit-reservation', 'data': {'status': True}}, client_sid)


msocketio.subscribe_on_type('celledit-reservation', update_meeting_cb)


def ack_email_sent_cb(value, opaque):
    msocketio.broadcast_message({'type': 'celledit-reservation', 'data': {'reload-table': True}})


mreservation.subscribe_end_user_ack_email_sent(ack_email_sent_cb, None)
mreservation.subscribe_end_user_survey_email_sent(ack_email_sent_cb, None)
mreservation.subscribe_end_user_email_send_retry(ack_email_sent_cb, None)
mreservation.subscribe_visit_enabled(ack_email_sent_cb, None)



table_configuration = {
    'view': 'reservation',
    'title': 'Reservaties',
    'buttons': [
        'edit', 'delete'
    ],
    'delete_message': u'Wilt u deze reservatie(s) verwijderen?',
    'template': [
        {'name': 'row_action', 'data': 'row_action', 'width': '2%'},

        {'name': 'Naam', 'data': 'full_name', 'order_by': EndUser.first_name, 'orderable': True},
        {'name': 'E-mail', 'data': 'end-user-email', 'order_by': EndUser.email, 'orderable': True},
        {'name': 'Profiel', 'data': 'profile_text', 'order_by': EndUser.profile, 'orderable': True},
        {'name': 'Code', 'data': 'code', 'order_by': EndUser.code, 'orderable': True},
        {'name': 'Invitatie', 'data': 'email_sent', 'order_by': EndUser.email_sent, 'orderable': True,
         'celltoggle': 'standard'},
        {'name': 'Survey', 'data': 'survey_email_sent', 'order_by': EndUser.email_sent, 'orderable': True,
         'celltoggle': 'standard'},
        {'name': 'Actief', 'data': 'enabled', 'order_by': EndUser.enabled, 'orderable': True,
         'celltoggle': 'standard'},
        {'name': 'Tx-retry', 'data': 'email-send-retry', 'order_by': EndUser.email_send_retry, 'orderable': True, 'celledit': 'text'},
    ],
    'filter': [],
    'item': {
        # 'edit': {'title': 'Wijzig een reservatie', 'buttons': ['save', 'cancel']},
        # 'view': {'title': 'Bekijk een reservatie', 'buttons': ['edit', 'cancel']},
        # 'add': {'title': 'Voeg een reservatie toe', 'buttons': ['save', 'cancel']},
    },
    'href': [],
    'pre_filter': mend_user.pre_filter,
    'format_data': mend_user.format_data,
    'search_data': mend_user.search_data,
    'default_order': (1, 'asc'),
    'socketio_endpoint': 'celledit-reservation',
    # 'cell_color': {'supress_cell_content': True, 'color_keys': {'X': 'red', 'O': 'green'}}, #TEST
    # 'suppress_dom': True,

}
