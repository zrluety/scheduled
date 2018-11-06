import json
import os

import click
import yaml

from .. import main


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'data'
    )
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
@click.option('-p', '--profile-json', help='path to json profile')
def refresh(profile_json):
    """Refresh the list of available profiles."""
    data = {}
    data["names"] = []
    profiles_dir = os.path.join(DATA_DIR, 'profiles')
    for file in os.listdir(profiles_dir):
        relpath = os.path.join(profiles_dir, file)
        with open(relpath, "r") as profile:
            p = yaml.load(profile)

        # add the name property of the configuration to the list. If the name
        # is not present, then use the filename as a default
        data["names"].append(p.get("name", os.path.splitext(file)[0]))

    with open(profile_json, "w") as outfile:
        json.dump(data, outfile)
