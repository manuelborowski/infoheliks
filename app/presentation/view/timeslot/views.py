from . import timeslot
from app import supervisor_required
from flask_login import login_required
from app.presentation.view import base_multiple_items
from app.application import reservation as mreservation, settings as msettings, socketio as msocketio


@timeslot.route('/timeslot', methods=['POST', 'GET'])
@login_required
@supervisor_required
def show():
    return base_multiple_items.show(table_configuration)


@timeslot.route('/timeslot/table_ajax', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_ajax():
    return base_multiple_items.ajax(table_configuration)


@timeslot.route('/timeslot/table_action', methods=['GET', 'POST'])
@login_required
@supervisor_required
def table_action():
    pass


table_configuration = {
    'view': 'timeslot',
    'title': 'Tijdsloten',
    'buttons': [],
    'delete_message': u'Wilt u dit/deze tijdslot(en) verwijderen?',
    'template': [
        {'name': 'row_action', 'data': 'row_action', 'width': '1%'},

        {'name': 'Tijdslot', 'data': 'timeslot', 'width': '10%'},
        {'name': 'Aantal gasten', 'data': 'nbr_visits','width': '3%'},
        {'name': 'Max gasten', 'data': 'max_visits', 'width': '3%'},
        {'name': 'Op de site', 'data': 'nbr_on_site', 'width': '3%'},
        {'name': 'In wonder', 'data': 'nbr_in_wonder', 'width': '3%'},
    ],
    'filter': [],
    'item': {
    },
    'href': [],
    'format_data': mreservation.format_timeslot_data,
    'default_order': (1, 'asc'),
    'socketio_endpoint': 'celledit-timeslot',
    # 'cell_color': {'supress_cell_content': True, 'color_keys': {'X': 'red', 'O': 'green'}}, #TEST
    # 'suppress_dom': True,
    'width': '40%'
}
