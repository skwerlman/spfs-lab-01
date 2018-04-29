import json
from unittest.mock import Mock

from nacl.secret import SecretBox
from nacl.public import PrivateKey
import pytest

from spfs.identities import Identity, IdentityManager
from spfs.utils import get_multihash
from spfs.wallets import Wallet


@pytest.fixture
def private_key():
    return PrivateKey.generate()


@pytest.fixture
def other_public_key():
    sk = PrivateKey.generate()
    return sk.public_key


@pytest.fixture
def username():
    return 'a user'


@pytest.fixture
def password():
    return 'a password'


@pytest.fixture
def wallet(username, password):
    key = f'{username}:{password}'.encode('utf-8')
    box = SecretBox(bytes.fromhex(get_multihash(key)))
    encrypted_data = box.encrypt(json.dumps({'test': True, 'opened': True}).encode('utf-8'))

    MockedWallet = type('MockedWallet', (Wallet,), {
        'get_data': Mock(return_value=encrypted_data),
        'persist_as_blocks': Mock(return_value=get_multihash(b'foobar'))
    })

    return MockedWallet({'test': True, 'created': True}, get_multihash(key))


@pytest.fixture
def identity(private_key):
    return Identity('test identity', private_key, {'test': True})


@pytest.fixture
def identity_manager(wallet):
    return IdentityManager(wallet)
