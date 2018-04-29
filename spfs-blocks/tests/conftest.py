from pathlib import PosixPath
from unittest.mock import Mock

import pytest

from spfs.utils import get_multihash
from spfs.blocks import Block


MockedBlock = type('MockedBlock', (Block,), {
    'persist_to_disk': Mock(),
    'retrieve_from_disk': Mock(return_value=b'DData supposedly on the disk, but really only mocked.')
})


@pytest.fixture
def block():
    return MockedBlock('it is a simple test of Block data'.encode('utf-8'))


@pytest.fixture
def real_block():
    return Block('that should be a real block, not mocked'.encode('utf-8'))


@pytest.fixture
def empty_block():
    return MockedBlock(b'')


@pytest.fixture
def inexistent_path():
    return PosixPath('/thats-very-improbable-such-a-entry-exists-on-developers-filesystem')


@pytest.fixture
def block_payload_type_X():
    return b'XDATA'


@pytest.fixture
def a_multihash():
    return get_multihash(b'a')
