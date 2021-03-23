from flask import render_template
from flask_login import login_required

from app import admin_required
from app.application import socketio as msocketio, utils as mutils
from . import settings
from app.application import settings as msettings


@settings.route('/settings', methods=['GET', 'POST'])
@admin_required
@login_required
def show():
    default_settings = msettings.get_configuration_settings()
    default_settings['timeslot-first-start'] = mutils.datetime_to_formiodate(default_settings['timeslot-first-start'])
    default_settings['timeslot-break-first-start'] = mutils.datetime_to_formiodate(default_settings['timeslot-break-first-start'])
    return render_template('/settings/settings.html',
                           settings_form=settings_formio, default_settings=default_settings)


def update_settings_cb(msg, client_sid=None):
    data = msg['data']
    if data['setting'] == 'timeslot-first-start' or data['setting'] == 'timeslot-break-first-start':
        data['value'] = mutils.formiodate_to_datetime(data['value'])
    msettings.set_configuration_setting(data['setting'], data['value'])


msocketio.subscribe_on_type('settings', update_settings_cb)

from app.presentation.view import false, true, null

# https://formio.github.io/formio.js/app/builder
settings_formio = \
    {
        "display": "form",
        "components": [
            {
                "title": "Algemeen",
                "theme": "primary",
                "collapsible": true,
                "key": "algemeen",
                "type": "panel",
                "label": "Algemeen",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Gasten worden toegelaten",
                        "tableView": false,
                        "persistent": false,
                        "key": "enable-enter-guest",
                        "type": "checkbox",
                        "input": true,
                        "defaultValue": false
                    },
                    {
                        "label": "Popup boodschap bij betreden van de site",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "enter-site-popup-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "Stage configuratie",
                "theme": "primary",
                "collapsible": true,
                "key": "stage2Configuratie",
                "type": "panel",
                "label": "Stage 2 configuratie",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Bezoeker stage 2 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Bezoeker-stage-2-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Bezoeker stage 3 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Bezoeker-stage-3-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Bezoeker stage 4 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Bezoeker-stage-4-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Schoolmedewerker stage 2 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Schoolmedewerker-stage-2-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Schoolmedewerker stage 3 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Schoolmedewerker-stage-3-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Schoolmedewerker stage 4 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Schoolmedewerker-stage-4-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Scholengemeenschapmedewerker stage 2 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Scholengemeenschapmedewerker-stage-2-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Scholengemeenschapmedewerker stage 3 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Scholengemeenschapmedewerker-stage-3-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Scholengemeenschapmedewerker stage 4 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Scholengemeenschapmedewerker-stage-4-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Test stage 2 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Test-stage-2-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Test stage 3 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Test-stage-3-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Test stage 4 vertraging",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "defaultValue": 0,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "Test-stage-4-delay",
                        "type": "number",
                        "labelWidth": 50,
                        "input": true
                    },
                    {
                        "label": "Infosessie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "infosession-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "Tijdslot configuratie",
                "theme": "primary",
                "collapsible": true,
                "key": "tijdslotConfiguratie",
                "type": "panel",
                "label": "Tijdslot configuratie",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Eerste tijdslot start om",
                        "labelPosition": "left-left",
                        "displayInTimezone": "location",
                        "allowInput": false,
                        "format": "dd/MM/yyyy HH:mm",
                        "tableView": false,
                        "enableMinDateInput": false,
                        "datePicker": {
                            "disableWeekends": false,
                            "disableWeekdays": false
                        },
                        "enableMaxDateInput": false,
                        "timePicker": {
                            "showMeridian": false
                        },
                        "persistent": false,
                        "key": "timeslot-first-start",
                        "type": "datetime",
                        "timezone": "Europe/London",
                        "input": true,
                        "widget": {
                            "type": "calendar",
                            "timezone": "Europe/London",
                            "displayInTimezone": "location",
                            "locale": "en",
                            "useLocaleSettings": false,
                            "allowInput": false,
                            "mode": "single",
                            "enableTime": true,
                            "noCalendar": false,
                            "format": "dd/MM/yyyy HH:mm",
                            "hourIncrement": 1,
                            "minuteIncrement": 1,
                            "time_24hr": true,
                            "minDate": null,
                            "disableWeekends": false,
                            "disableWeekdays": false,
                            "maxDate": null
                        }
                    },
                    {
                        "label": "Lengte van een tijdslot",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "timeslot-length",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Aantal tijdsloten",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "timeslot-number",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Aantal gasten per tijdslot",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "timeslot-max-guests",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Pauze tijdslot start om",
                        "labelPosition": "left-left",
                        "displayInTimezone": "location",
                        "allowInput": false,
                        "format": "dd/MM/yyyy HH:mm",
                        "tableView": false,
                        "enableMinDateInput": false,
                        "datePicker": {
                            "disableWeekends": false,
                            "disableWeekdays": false
                        },
                        "enableMaxDateInput": false,
                        "timePicker": {
                            "showMeridian": false
                        },
                        "persistent": false,
                        "key": "timeslot-break-first-start",
                        "type": "datetime",
                        "timezone": "Europe/London",
                        "input": true,
                        "widget": {
                            "type": "calendar",
                            "timezone": "Europe/London",
                            "displayInTimezone": "location",
                            "locale": "en",
                            "useLocaleSettings": false,
                            "allowInput": false,
                            "mode": "single",
                            "enableTime": true,
                            "noCalendar": false,
                            "format": "dd/MM/yyyy HH:mm",
                            "hourIncrement": 1,
                            "minuteIncrement": 1,
                            "time_24hr": true,
                            "minDate": null,
                            "disableWeekends": false,
                            "disableWeekdays": false,
                            "maxDate": null
                        }
                    },
                    {
                        "label": "Aantal pauze tijdsloten",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "timeslot-break-number",
                        "type": "number",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "BEZOEKERS : Registratie template en e-mail",
                "theme": "primary",
                "collapsible": true,
                "key": "RegistratieTemplate1",
                "type": "panel",
                "label": "BEZOEKERS : Registratie template en e-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Web registratie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "register-guest-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-guest-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-guest-mail-ack-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "VLOER MEDEWERKERS : Registratie template en e-mail",
                "theme": "primary",
                "collapsible": true,
                "key": "RegistratieTemplate2",
                "type": "panel",
                "label": "MEDEWERKERS : Registratie template en e-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Web registratie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "register-floor-coworker-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-floor-coworker-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-floor-coworker-mail-ack-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "SCHOOL MEDEWERKERS : Registratie template en e-mail",
                "theme": "primary",
                "collapsible": true,
                "key": "RegistratieTemplate3",
                "type": "panel",
                "label": "VLOER MEDEWERKERS : Registratie template en e-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Web registratie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "register-fair-coworker-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-fair-coworker-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-fair-coworker-mail-ack-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "Registratie template en e-mail",
                "theme": "primary",
                "collapsible": true,
                "hidden": true,
                "key": "RegistratieTemplate",
                "type": "panel",
                "label": "Registratie template en e-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Web registratie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "register-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-mail-ack-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "Teams-meeting bevestigingse-mail",
                "theme": "primary",
                "collapsible": true,
                "hidden": true,
                "key": "teamsMeetingBevestigingseMail",
                "type": "panel",
                "label": "Teams-meeting bevestigingse-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "meeting-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "meeting-mail-ack-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "INFOSESSIE: items templates",
                "theme": "primary",
                "collapsible": true,
                "key": "teamsMeetingBevestigingseMail1",
                "type": "panel",
                "label": "Infosessie: items templates",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Embedded video template",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "embedded-video-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Chatroom template",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "chat-room-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Floating video template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "floating-video-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Floating document template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "floating-document-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Link template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "link-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Wonder Link template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "wonder-link-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Infosessie items json",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "infosession-content-json",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "Enquête template",
                "theme": "primary",
                "collapsible": true,
                "key": "teamsMeetingBevestigingseMail2",
                "type": "panel",
                "label": "INFOSESSIE: items templates",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Enquête template",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "survey-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Enquête standaard antwoorden template",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "survey-default-results-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Enquête uitnodingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "survey-mail-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Enquête uitnodigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "survey-mail-content-template",
                        "type": "textarea",
                        "input": true
                    }
                ],
                "collapsed": true
            },
            {
                "title": "E-mail server settings",
                "theme": "primary",
                "collapsible": true,
                "key": "eMailServerSettings",
                "type": "panel",
                "label": "E-mail server settings",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Aantal keer dat een e-mail geprobeerd wordt te verzenden",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": false,
                        "tableView": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "email-send-max-retries",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Tijd (seconden) tussen het verzenden van e-mails",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "persistent": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "email-task-interval",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Max aantal e-mails per minuut",
                        "labelPosition": "left-left",
                        "mask": false,
                        "spellcheck": true,
                        "tableView": false,
                        "persistent": false,
                        "delimiter": false,
                        "requireDecimal": false,
                        "inputFormat": "plain",
                        "key": "emails-per-minute",
                        "type": "number",
                        "input": true
                    },
                    {
                        "label": "Basis URL",
                        "labelPosition": "left-left",
                        "tableView": true,
                        "key": "base-url",
                        "type": "textfield",
                        "input": true
                    },
                    {
                        "label": "E-mails mogen worden verzonden",
                        "tableView": false,
                        "persistent": false,
                        "key": "enable-send-email",
                        "type": "checkbox",
                        "input": true,
                        "defaultValue": false
                    }
                ],
                "collapsed": true
            }
        ]
    }