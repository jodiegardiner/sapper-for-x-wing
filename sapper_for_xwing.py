from flask import Flask, render_template
import requests
import json
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
def ship_processor():
    def get_ship_icon(pilot):


        return u'url_for_icon.jpg'
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
    r = requests.get(api + id)
    data = r.json()
    print(data)

    for player in data['participants']:
        print(player)

        if player['list_json']:
            player['list_json'] = json.loads(player['list_json'])
            # player['list_json']['faction'] = map_icon(player['list_json']['faction'])
            if player['list_json']['vendor']:
                for v in player['list_json']['vendor']:
                    try:
                        player['link'] = player['list_json']['vendor'][v]['link']
                    except:
                        player['link'] = 'No link'
            else:
                player['link'] = "No link"

    print(data)

    return render_template('event.html', event=data, api=api)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
