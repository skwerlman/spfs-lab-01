import sys

import click

from spfs.json import json
from . import cli


@click.group()
def cmds():
    pass


@cmds.command()
@click.argument('name')
def create(name):
    manager = cli.open_manager()
    identity = manager.create(name)
    cli.persist_manager(manager)

    print(identity.data)


@cmds.command()
def list():
    manager = cli.open_manager()
    for name, identity in manager.identities.items():
        print(name, ':', identity.data)


@cmds.command()
@click.argument('name')
def open(name):
    manager = cli.open_manager()
    identity = manager.identities[name]
    print(identity.data)


@cmds.command()
@click.argument('name')
@click.argument('key')
def get(name, key):
    manager = cli.open_manager()

    if name not in manager.identities:
        sys.exit(404)

    identity = manager.identities[name]
    if key not in identity.data:
        sys.exit(404)

    print(identity.data[key])


@cmds.command()
@click.argument('name')
@click.argument('key')
@click.argument('value')
def set(name, key, value):
    manager = cli.open_manager()
    identity = manager.identities[name]
    identity.data[key] = json.loads(value)

    cli.persist_manager(manager)

    print(identity.data[key])


cmds()
