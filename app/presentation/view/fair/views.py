from . import fair
from app import admin_required, log, supervisor_required
from flask import redirect, url_for, request, render_template
from flask_login import login_required
from app.presentation.view import base_multiple_items
from app.data import reservation as mdreservation, fair as mdfair
from app.application import reservation as mreservation, settings as msettings, socketio as msocketio, fair as mfair
from app.data.models import SchoolReservation, AvailablePeriod, EndUser, Visit, Fair

from app.presentation.layout.utils import flash_plus, button_pressed
from app.presentation.view import update_available_periods, false, true, null, prepare_registration_form

import json


@fair.route('/fair', methods=['POST', 'GET'])
@login_required
@supervisor_required
def show():
    return base_multiple_items.show(table_configuration)


@fair.route('/fair/table_ajax', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_ajax():
    return base_multiple_items.ajax(table_configuration)


@fair.route('/fair/table_action', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_action():
    pass

def update_fair_cb(msg, client_sid=None):
    if msg['data']['column'] == 2: # wonder room url
        mfair.update_fair_by_id(msg['data']['id'], msg['data']['value'])
    msocketio.send_to_room({'type': 'celledit-fair', 'data': {'status': True}}, client_sid)

msocketio.subscribe_on_type('celledit-fair', update_fair_cb)




table_configuration = {
    'view': 'fair',
    'title': 'Scholen',
    'buttons': [],
    'delete_message': '',
    'template': [
        {'name': 'row_action', 'data': 'row_action', 'width': '2%'},

        {'name': 'School', 'data': 'school', 'order_by': Fair.school, 'orderable': True},
        # {'name': 'Wonder', 'data': 'wonder_url', 'order_by': Fair.school, 'orderable': True, 'celledit': 'text'},
    ],
    'filter': [],
    'item': {},
    'href': [],
    'pre_filter': mdfair.pre_filter,
    'format_data': mdfair.format_data,
    'search_data': mdfair.search_data,
    'default_order': (1, 'asc'),
    'socketio_endpoint': 'celledit-fair',
    # 'cell_color': {'supress_cell_content': True, 'color_keys': {'X': 'red', 'O': 'green'}}, #TEST
    # 'suppress_dom': True,
    'width' : '50%',
}
