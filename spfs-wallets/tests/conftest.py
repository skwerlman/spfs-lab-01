import json
from unittest.mock import Mock

from nacl.secret import SecretBox
import pytest

from spfs.utils import get_multihash
from spfs.wallets import Wallet


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
