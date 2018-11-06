import json
import os

import yaml


def update_profiles_list():
    data = {}
    data['names'] = []
    for file in os.listdir('./profiles'):
        relpath = os.path.join('./profiles', file)
        with open(relpath, 'r') as profile:
            p = yaml.load(profile)

        # add the name property of the configuration to the list. If the name
        # is not present, then use the filename as a default
        data['names'].append(p.get('name', os.path.splitext(file)[0]))

    with open('./workbooks/profiles.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    update_profiles_list()

