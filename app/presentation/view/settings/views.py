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
    default_settings['site-open-at'] = mutils.datetime_to_formiodate(default_settings['site-open-at'])
    return render_template('/settings/settings.html',
                           settings_form=settings_formio, default_settings=default_settings)


def update_settings_cb(msg, client_sid=None):
    data = msg['data']
    if data['setting'] == 'site-open-at':
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
                        "label": "Bevraging activeren",
                        "tableView": false,
                        "defaultValue": false,
                        "persistent": false,
                        "key": "enable-send-survey-email",
                        "type": "checkbox",
                        "input": true
                    },
                    {
                        "label": "Site opent op",
                        "labelPosition": "left-left",
                        "displayInTimezone": "utc",
                        "format": "yyyy-MM-dd HH:mm",
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
                        "defaultValue": "2021-05-03T19:00:00+02:00",
                        "key": "site-open-at",
                        "type": "datetime",
                        "input": true,
                        "widget": {
                            "type": "calendar",
                            "displayInTimezone": "utc",
                            "locale": "en",
                            "useLocaleSettings": false,
                            "allowInput": true,
                            "mode": "single",
                            "enableTime": true,
                            "noCalendar": false,
                            "format": "yyyy-MM-dd HH:mm",
                            "hourIncrement": 1,
                            "minuteIncrement": 1,
                            "time_24hr": true,
                            "minDate": null,
                            "disableWeekends": false,
                            "disableWeekdays": false,
                            "maxDate": null
                        }
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
                "title": "MEDEWERKERS : Registratie template en e-mail",
                "theme": "primary",
                "collapsible": true,
                "key": "RegistratieTemplate2",
                "type": "panel",
                "label": "VLOER MEDEWERKERS : Registratie template en e-mail",
                "input": false,
                "tableView": false,
                "components": [
                    {
                        "label": "Web registratie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "register-coworker-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: onderwerp",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-coworker-mail-ack-subject-template",
                        "type": "textarea",
                        "input": true
                    },
                    {
                        "label": "Registratie bevestigingse-mail: inhoud",
                        "autoExpand": false,
                        "tableView": true,
                        "persistent": false,
                        "key": "register-coworker-mail-ack-content-template",
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
                        "label": "Infosessie template",
                        "autoExpand": false,
                        "tableView": true,
                        "key": "infosession-template",
                        "type": "textarea",
                        "input": true
                    },
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