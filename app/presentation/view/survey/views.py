from . import survey
from app import admin_required, log, supervisor_required
from flask import redirect, url_for, request, render_template
from flask_login import login_required
from app.presentation.view import base_multiple_items
from app.data import survey as msurvey
from app.application import reservation as mreservation, settings as msettings, socketio as msocketio
from app.data.models import SchoolReservation, AvailablePeriod, EndUserSurvey
from app.presentation.layout.utils import flash_plus, button_pressed
from app.presentation.view import update_available_periods, false, true, null, prepare_registration_form

import json


@survey.route('/survey', methods=['POST', 'GET'])
@login_required
@supervisor_required
def show():
    return base_multiple_items.show(table_configuration)


@survey.route('/survey/table_ajax', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_ajax():
    return base_multiple_items.ajax(table_configuration)


@survey.route('/survey/table_action', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_action():
    pass


table_configuration = {
    'view': 'survey',
    'title': 'Bevragingen',
    'buttons': [],
    'delete_message': '',
    'template': [
        {'name': 'row_action', 'data': 'row_action', 'width': '2%'},

        {'name': 'Woonplaats', 'data': 'city', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'School', 'data': 'school', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Broodzak', 'data': 'information-channel.broodzak', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Infoborden', 'data': 'information-channel.infoborden', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'School', 'data': 'information-channel.school', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Andere', 'data': 'information-channel.andere', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Informatiekanaal andere', 'data': 'information-channel-other', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Introfilm', 'data': 'stage-2-score.intro-movie', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'CLB', 'data': 'stage-2-score.clb-info', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'SG', 'data': 'stage-2-score.scholengemeenschap-info', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'SALI', 'data': 'stage-2-score.internaat-info', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Chat', 'data': 'stage-2-score.chat-info', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Deel één feedback', 'data': 'stage-2-feedback', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Vragen stellen', 'data': 'stage-3-score.able-to-ask-questions', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Video chat', 'data': 'stage-3-score.video-chat-experience', 'order_by': EndUserSurvey.code, 'orderable': True},
        {'name': 'Deel twee feedback', 'data': 'stage-3-feedback', 'order_by': EndUserSurvey.code, 'orderable': True},
    ],
    'filter': [],
    'item': {},
    'href': [],
    'pre_filter': msurvey.pre_filter,
    'format_data': msurvey.format_data,
    'search_data': msurvey.search_data,
    'default_order': (1, 'asc'),
    'socketio_endpoint': 'celledit-reservation',
    # 'cell_color': {'supress_cell_content': True, 'color_keys': {'X': 'red', 'O': 'green'}}, #TEST
    # 'suppress_dom': True,
    'export_excel_button': True,
}
