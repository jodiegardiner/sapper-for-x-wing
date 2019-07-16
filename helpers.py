import os
import json


def build_ship_json():
    ships = {}
    for root, dirs, files in os.walk('xwing-data2/data/pilots'):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                full_json = json.load(auto)

                print(full_json)


def search_ship_json(name):
    for root, dirs, files in os.walk('xwing-data2/data/pilots'):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                full_json = json.load(auto)
                # print(full_json['xws'])
                try:
                    if full_json['xws'] == str(name):
                        return full_json['icon']
                    # print(full_json)
                except:
                    continue

build_ship_json()

# search_ship_json('tiesffighter')
