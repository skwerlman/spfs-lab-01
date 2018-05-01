from os import environ

from nacl.secret import SecretBox

from spfs import settings
from spfs.blocks import Block
from spfs.json import json
from spfs.objects import serialize
from spfs.utils import get_multihash
from . import Wallet


wallets_link = settings.spfs_home / 'wallets.link'
wallets_keys = settings.spfs_home / 'wallets.keys'


def get_wallets_box():
    password = environ.get('WALLETS_PASSWORD', None)
    if password is None:
        raise ValueError('You should set a WALLETS_PASSWORD environment variable')

    password_multihash = get_multihash(password.encode('utf-8'))
    return SecretBox(bytes.fromhex(password_multihash))


def list_wallets():
    if not wallets_link.exists():
        return {}

    with wallets_link.open() as file_obj:
        multihash = file_obj.read()
        serialized_data = Block.get_data(multihash)
        return json.loads(serialized_data)


def add_to_wallets_list(name, multihash):
    wallets_list = list_wallets()
    wallets_list[name] = multihash
    return save_as_wallets_list(wallets_list)


def save_as_wallets_list(wallets_list):
    serialized_data = serialize(wallets_list)
    multihash = Block.persist_data(serialized_data)
    update_wallets_link(multihash)

    return multihash


def get_wallet_name(multihash):
    for name, wallet_multihash in list_wallets():
        if wallet_multihash == multihash:
            return name


def update_wallets_link(multihash):
    with wallets_link.open('w') as file_obj:
        file_obj.write(multihash)


def open_wallet(key, name):
    multihash = list_wallets()[name]
    return Wallet.open_with_key(key, multihash)


############################
def list_wallets_keys():
    if not wallets_keys.exists():
        return {}

    with wallets_keys.open('rb') as file_obj:
        encrypted_data = file_obj.read()
        serialized_data = get_wallets_box().decrypt(encrypted_data)
        return json.loads(serialized_data)


def add_to_wallets_keys(name, key):
    wallets_keys = list_wallets_keys()
    wallets_keys[name] = key
    return save_as_wallets_keys(wallets_keys)


def save_as_wallets_keys(wallets_keys):
    serialized_data = serialize(wallets_keys)
    update_wallets_keys(serialized_data)


def update_wallets_keys(serialized_data):
    encrypted_data = get_wallets_box().encrypt(serialized_data)
    with wallets_keys.open('wb') as file_obj:
        file_obj.write(encrypted_data)


def get_wallet_key(name):
    wallets_keys = list_wallets_keys()
    return wallets_keys[name]
