import sys

import click

from spfs.json import json
from spfs.identities import IdentityManager
from spfs.wallets import cli as wallets_cli


def open_wallet(name):
    wallet_key = wallets_cli.get_wallet_key(name)
    return wallets_cli.open_wallet(wallet_key, name)


_wallet = None


def open_manager():
    global _wallet
    if _wallet is None:
        wallets = wallets_cli.list_wallets()
        keys = tuple(wallets.keys())
        if len(keys) == 0:
            raise Exception('You must create a wallet, first.')
        wallet_name = keys[0]
        _wallet = open_wallet(wallet_name)
        _wallet.name = wallet_name
        print(f'Using Wallet "{wallet_name}"')
    return IdentityManager(_wallet)


def persist_manager(manager):
    wallet_multihash = manager.persist()
    wallets_cli.add_to_wallets_list(manager.wallet.name, wallet_multihash)


##################################################
@click.group()
def cmds():
    pass


@cmds.command()
@click.argument('name')
def create(name):
    manager = open_manager()
    identity = manager.create(name)
    persist_manager(manager)

    print(identity.data)


@cmds.command()
def list():
    manager = open_manager()
    for name, identity in manager.identities.items():
        print(name, ':', identity.data)


@cmds.command()
@click.argument('name')
def open(name):
    manager = open_manager()
    identity = manager.identities[name]
    print(identity.data)


@cmds.command()
@click.argument('name')
@click.argument('key')
def get(name, key):
    manager = open_manager()
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
    manager = open_manager()
    identity = manager.identities[name]
    identity.data[key] = json.loads(value)

    persist_manager(manager)

    print(identity.data[key])


cmds()
