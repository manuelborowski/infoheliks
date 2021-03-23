from app.application import reservation as mreservation, settings as msettings, enter as menter, utils as mutils, room as mroom
from app import flask_app
import json, re

false = False
true = True
null = None


def prepare_registration_form(code=None, id=None):
    ret = mreservation.get_default_values(code, id)
    if ret.result == ret.Result.E_OK:
        if 'timeslots' in ret.registration:
            update_timeslots(ret.registration['timeslots'], ret.registration['template'], 'radio-visit-timeslots')
        if 'floors' in ret.registration:
            update_floors(ret.registration['floors'], ret.registration['template'], 'radio-floor-levels')
        if 'fairs' in ret.registration:
            update_fairs(ret.registration['fairs'], ret.registration['template'], 'radio-fair-schools')
    return ret


def update_timeslots(timeslots, form, key):
    components = form['components']
    for component in components:
        if 'key' in component and component['key'] == key:
            value_template = component['values'][0]
            component['values'] = []
            for timeslot in timeslots:
                if timeslot['nbr_visits_available'] <= 0:
                    continue
                new_value = dict(value_template)
                new_value['label'] = timeslot['label']
                new_value['value'] = timeslot['value']
                component['values'].append(new_value)
            return
        if 'components' in component:
            update_timeslots(timeslots, component, key)
    return


def update_floors(floors, form, key):
    components = form['components']
    for component in components:
        if 'key' in component and component['key'] == key:
            value_template = component['values'][0]
            component['values'] = []
            for floor in floors:
                new_value = dict(value_template)
                new_value['label'] = floor['label']
                new_value['value'] = floor['value']
                component['values'].append(new_value)
            return
        if 'components' in component:
            update_floors(floors, component, key)
    return


def update_fairs(fairs, form, key):
    components = form['components']
    for component in components:
        if 'key' in component and component['key'] == key:
            value_template = component['values'][0]
            component['values'] = []
            for fair in fairs:
                new_value = dict(value_template)
                new_value['label'] = fair['label']
                new_value['value'] = fair['value']
                component['values'].append(new_value)
            return
        if 'components' in component:
            update_floors(fairs, component, key)
    return


def update_available_periods(periods, form, key):
    components = form['components']
    for component in components:
        if 'key' in component and component['key'] == key:
            select_template = component['components'][0]
            data_template = component['components'][0]['data']['values'][0]
            component['components'] = []
            for period in periods:
                if period['boxes_available'] <= 0:
                    continue
                new = dict(select_template)
                new['data'] = dict({'values': []})
                for value in range(period['boxes_available'] + 1):
                    new_data = dict(data_template)
                    new_data['label'] = str(value)
                    new_data['value'] = str(value)
                    new['data']['values'].append(new_data)
                new['label'] = period['period']
                new['key'] = f'select-boxes-{period["id"]}'
                component['components'].append(new)
            return
        if 'components' in component:
            update_available_periods(periods, component, key)
    return


def prepare_enter_form(code):
    #recursive
    def process_items(parent, items):
        for item in items:
            type = item['type']
            child = None
            if type == 'content':
                child = mutils.deepcopy(formio_component_templates['content'])
                child['html'] = item['text']
            elif type == 'embedded-video':
                child = mutils.deepcopy(formio_component_templates['content'])
                youtube_id = get_youtube_id_from_url(item['url'])
                url = f'https://www.youtube.com/embed/{youtube_id}'
                play_options = []
                if 'autostart' in item and item['autostart']:
                    play_options.append('autoplay=1&mute=1')
                if 'loop' in item and item['loop']:
                    play_options.append(f'playlist={youtube_id}&loop=1')
                if play_options:
                    url = f'{url}?{"&".join(play_options)}'
                title = item["title"] if 'title' in item else ''
                tooltip = get_tooltip_from_item(item)
                html = embedded_video_template.replace('{{URL-TAG}}', url)
                html = html.replace('{{TITLE-TAG}}', title)
                child['html'] = html.replace('{{TOOLTIP-TAG}}', tooltip)
            elif type == 'chat-room':
                child = mutils.deepcopy(formio_component_templates['content'])
                title, id = mroom.get_chat_room_configuration(item['id'], ret.ret['user'])
                html = chat_room_template.replace('{{TITLE-TAG}}', title)
                child['html'] = html.replace('{{ID-TAG}}', id)
            elif type == 'floating-video':
                child = mutils.deepcopy(formio_component_templates['content'])
                tooltip = get_tooltip_from_item(item)
                html = floating_video_template.replace('{{TITLE-TAG}}', item['title'])
                html = html.replace('{{TOOLTIP-TAG}}', tooltip)
                youtube_id = get_youtube_id_from_url(item['url'])
                html = html.replace('{{THUMB-URL-TAG}}', f'https://img.youtube.com/vi/{youtube_id}/sddefault.jpg')
                child['html'] = html.replace('{{URL-TAG}}', f'https://www.youtube.com/watch?v={youtube_id}')
            elif type == 'floating-document':
                child = mutils.deepcopy(formio_component_templates['content'])
                tooltip = get_tooltip_from_item(item)
                thumbnail_link = google_drive_link_to_thumbnail(item)
                html = floating_document_template.replace('{{TITLE-TAG}}', item['title'])
                html = html.replace('{{TOOLTIP-TAG}}', tooltip)
                html = html.replace('{{THUMB-URL-TAG}}', thumbnail_link)
                child['html'] = html.replace('{{URL-TAG}}', item['url'])
            elif type == 'link':
                child = mutils.deepcopy(formio_component_templates['content'])
                tooltip = get_tooltip_from_item(item)
                thumbnail_link = google_drive_link_to_thumbnail(item)
                html = link_template.replace('{{TITLE-TAG}}', item['title'])
                html = html.replace('{{TOOLTIP-TAG}}', tooltip)
                html = html.replace('{{THUMB-URL-TAG}}', thumbnail_link)
                child['html'] = html.replace('{{URL-TAG}}', item['url'])
            elif type == 'columns':
                child = mutils.deepcopy(formio_component_templates['columns'])
                for column in item['columns']:
                    column_template = mutils.deepcopy(formio_component_templates['columns-column'])
                    column_template['width'] = column['width']
                    process_items(column_template['components'], column['content'])
                    child['columns'].append(column_template)
            elif type == 'panel':
                child = mutils.deepcopy(formio_component_templates['panel'])
                child['title'] = item['title']
                child['key'] = f"key-{item['title'].replace(' ', '-')}"
                process_items(child['components'], item['components'])
            elif type == 'wonder-url':
                child = mutils.deepcopy(formio_component_templates['panel'])
                child['collapsed'] = False
                child['collapsible'] = False
                child['title'] = item['title']
                wonder_links = menter.get_wonder_links(ret.ret['user'])
                for link in wonder_links:
                    inner_child = mutils.deepcopy(formio_component_templates['content'])
                    template = mutils.deepcopy(wonder_link_template)
                    template = template.replace('{{URL-TAG}}', link['link']).replace('{{TIMESLOT-TAG}}', link['timeslot'])
                    inner_child['html'] = template
                    child['components'].append(inner_child)
            parent.append(child)
        return parent

    ret = menter.end_user_wants_to_enter(code)
    if ret.ret:
        embedded_video_template = msettings.get_embedded_video_template()
        chat_room_template = msettings.get_chat_room_template()
        floating_video_template = msettings.get_floating_video_template()
        floating_document_template = msettings.get_floating_document_template()
        link_template = msettings.get_link_template()
        wonder_link_template = msettings.get_wonder_link_template()
        template = ret.ret['template']
        for tab, items in ret.ret['tabpages'].items():
            tab_component = search_component(template, tab)
            if tab_component:
                process_items(tab_component['components'], items)
    return ret


def search_component(form, key):
    components = form['components']
    for component in components:
        if 'key' in component and component['key'] == key:
            return component
        if 'components' in component:
            found_component = search_component(component, key)
            if found_component: return found_component
    return None


formio_component_templates = {
    'panel': {
        "collapsible": true,
        "key": "panel2",
        "type": "panel",
        "label": "Dummy Label",
        "input": false,
        "tableView": false,
        "components": [],
        "collapsed": true
    },
    'content': {
        "html": "",
        "label": "Content",
        "refreshOnChange": false,
        "key": "content",
        "type": "content",
        "input": false,
        "tableView": false,
    },
    'columns': {
        "label": "Columns",
        "columns": [],
        "key": "columns",
        "type": "columns",
        "input": false,
        "tableView": false
    },
    'columns-column': {
            "components": [],
            "width": 3,
            "offset": 0,
            "push": 0,
            "pull": 0,
            "size": "md"
        },
}

# in: https://drive.google.com/file/d/1q219q5dDRym0v6IxiqtX-CV1ZelMerW3/view?usp=sharing
# out: https://drive.google.com/thumbnail?id=1q219q5dDRym0v6IxiqtX-CV1ZelMerW3
def google_drive_link_to_thumbnail(item):
    if 'thumb-url' in item:
        match = re.match('.+drive.google.com\/file\/d\/(.+)\/', item['thumb-url'])
        image_link = f'https://drive.google.com/thumbnail?id={match.group(1)}'
        return image_link
    return 'https://drive.google.com/thumbnail?id=1ExD-sGRE-7XVz3qkhwMd8lIMEcBoap4u'


def get_tooltip_from_item(item):
    tooltip = f'title="{item["tooltip"]}"' if 'tooltip' in item else f'title="{item["title"]}"' if 'title' in item else ''
    return tooltip


def get_youtube_id_from_url(url):
    try:
        youtube_id = url.split('v=')[1]
    except:
        youtube_id = url.split('be/')[1]
    return youtube_id


def prepare_survey_form(code):

    ret = menter.end_user_wants_to_enter(code)
    if ret.ret:
        embedded_video_template = msettings.get_embedded_video_template()
        chat_room_template = msettings.get_chat_room_template()
        floating_video_template = msettings.get_floating_video_template()
        floating_document_template = msettings.get_floating_document_template()
        link_template = msettings.get_link_template()
        wonder_link_template = msettings.get_wonder_link_template()
        template = ret.ret['template']
        for tab, items in ret.ret['tabpages'].items():
            tab_component = search_component(template, tab)
            if tab_component:
                process_items(tab_component['components'], items)
    return ret