import json
import os

import click
import yaml

from .. import main


RESOURCES_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        'resources'
    )
)

WORKBOOKS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(RESOURCES_DIR)),
    'workbooks'
)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("profile")
@click.argument("src")
@click.argument("dst")
def run(profile, src, dst):
    main.run(profile, src, dst)


@cli.command()
def refresh():
    data = {}
    data["names"] = []
    profiles_dir = os.path.join(RESOURCES_DIR, 'profiles')
    for file in os.listdir(profiles_dir):
        relpath = os.path.join(profiles_dir, file)
        with open(relpath, "r") as profile:
            p = yaml.load(profile)

        # add the name property of the configuration to the list. If the name
        # is not present, then use the filename as a default
        data["names"].append(p.get("name", os.path.splitext(file)[0]))

    profiles_json = os.path.join(WORKBOOKS_DIR, 'profiles.json')
    with open(profiles_json, "w") as outfile:
        json.dump(data, outfile)
