from getpass import getpass

import click

from spfs.json import json
from spfs.utils import get_multihash
from . import Wallet
from . import cli


##################################################
@click.group()
def cmds():
    pass


@cmds.command()
@click.argument('name')
def create(name):
    password = getpass(f'Your password for "{name}" Wallet: ')
    key = get_multihash(f'{name}:{password}'.encode('utf-8'))

    wallet = Wallet({}, key)
    multihash = wallet.persist()
    print(f'Wallet address: {multihash}')

    cli.add_to_wallets_list(name, multihash)
    cli.add_to_wallets_keys(name, key)


@cmds.command()
@click.argument('name')
def key(name):
    print(cli.get_wallet_key(name))


@cmds.command()
@click.argument('name')
def open(name):
    key = cli.get_wallet_key(name)
    multihash = cli.list_wallets()[name]
    wallet = Wallet.open_with_key(key, multihash)
    print(wallet.data)


@cmds.command()
@click.argument('name')
@click.argument('key')
@click.argument('value')
def set(name, key, value):
    key = cli.get_wallet_key(name)
    multihash = cli.list_wallets()[name]
    wallet = Wallet.open_with_key(key, multihash)

    wallet.data[key] = json.loads(value)
    new_multihash = wallet.persist()
    cli.add_to_wallets_list(name, new_multihash)

    print(wallet.data)


@cmds.command()
@click.argument('name')
@click.argument('key')
def unset(name, key):
    key = cli.get_wallet_key(name)
    multihash = cli.list_wallets()[name]
    wallet = Wallet.open_with_key(key, multihash)

    if key in wallet.data:
        del wallet.data[key]
    new_multihash = wallet.persist()
    cli.add_to_wallets_list(name, new_multihash)

    print(wallet.data)


@cmds.command()
def list():
    wallets_list = cli.list_wallets()
    for key, value in wallets_list.items():
        print(f'{value}:{key}')


@cmds.command()
def list_keys():
    wallets_keys = cli.list_wallets_keys()
    for key, value in wallets_keys.items():
        print(f'{key}:{value}')


cmds()
