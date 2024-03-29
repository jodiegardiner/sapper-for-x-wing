from flask import Flask, render_template
import requests
import json
import os
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

icon_map = {
    'galacticempire': 'empire_icon.png',
    'rebelalliance': 'rebel_icon.png',
    'scumandvillainy': 'scum_icon.png',
    'separatistalliance': 'separatist_icon.png',
    'resistance': 'resistance_icon.png',
    'firstorder': 'firstorder_icon.png',
    'galacticrepublic': 'republic_icon.png'
}


def map_icon(faction):
    if faction in icon_map:
        return icon_map[faction]
    else:
        return faction


@app.context_processor
def utility_processor():
    def get_faction_icon(faction):
        icon = map_icon(faction)
        return u'{0}'.format(icon)

    return dict(get_faction_icon=get_faction_icon)


@app.context_processor
def utility_processor():
    def get_ship_icon(name):
        # print(os.path.join('Applications','PyCharm.app', 'Contents', 'bin', 'xwing-data', 'data', 'pilots'))
        # print(os.getcwd())
        for root, dirs, files in os.walk('/Users/jodie/funstuff/sapper_for_xwing/xwing-data2/data/pilots'):
            for file in files:
                with open(os.path.join(root, file), "r") as auto:
                    full_json = json.load(auto)
                    # print(full_json)
                    try:
                        if full_json['xws'] == str(name):
                            return u'{0}'.format(full_json['icon'])
                            # print(full_json)
                    except:
                        continue

    return dict(get_ship_icon=get_ship_icon)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events')
@app.route('/events/')
def tournaments():
    api = 'https://listfortress.com/api/v1/tournaments/'
    r = requests.get(api)
    data = r.json()
    print(data)

    # for event in data:
    #     r = requests.get(api + '{0}'.format(event['id']))
    #     eventdata = r.json()
    #     event['size'] = len(eventdata['participants'])
    return render_template('list.html', data=data, api=api)


@app.route('/events/<id>')
def event(id):
    api = 'https://listfortress.com/api/v1/tournaments/'

    if not id:
        data = []
        return render_template('list.html', data=data, api=api, error="You must provide an ID")

    r = requests.get(api + id)
    data = r.json()
    for player in data.get('participants', ''):
        print(player)

        if player['list_json']:
            player['list_json'] = json.loads(player['list_json'])
            # player['list_json']['faction'] = map_icon(player['list_json']['faction'])
            try:
                if player['list_json']['vendor']:
                    for v in player['list_json']['vendor']:
                        try:
                            player['link'] = player['list_json']['vendor'][v]['link']
                        except:
                            player['link'] = 'No link'
                else:
                    player['link'] = "No link"
            except:
                player['link'] = "Unrecognised Vendor"

    print(data)

    return render_template('event.html', event=data, api=api)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
