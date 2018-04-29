import pytest

from spfs import constants
from spfs.blocks import Block
from spfs.blocks.exceptions import BlockNotFoundError
from spfs.utils import get_multihash


def test_block_instantiation(block):
    assert block.multihash is not None
    assert len(block.multihash) == 64


def test_block_multihash(block):
    assert block.multihash == get_multihash(block.type + block.data)


def test_block_str(block):
    s = str(block)
    assert str(block.multihash) in s
    assert str(block.type) in s


def test_block_generate_payload_with_unicode_data(block):
    block.data = 'a unicode string'
    with pytest.raises(TypeError):
        block.generate_payload()


def test_block_generate_payload_with_unicode_type(block):
    block.type = 'x'
    with pytest.raises(TypeError):
        block.generate_payload()


def test_block_generate_payload_too_big(block):
    block.data = (b'x' * constants.BLOCK_MAX_SIZE) + b'-----'
    with pytest.raises(ValueError):
        block.generate_payload()


def test_block_retrieve_inexistent_from_disk(inexistent_path, real_block):
    with pytest.raises(BlockNotFoundError):
        real_block.retrieve_from_disk(inexistent_path)


def test_block_retrieve(block, a_multihash):
    retrieved_block = block.retrieve(a_multihash)
    assert len(block.retrieve_from_disk.call_args_list) > 0
    args, kwargs = block.retrieve_from_disk.call_args_list[0]
    str_path = str(args[0])
    assert a_multihash in str_path

    assert retrieved_block.type == b'D'
    assert retrieved_block.data == b'Data supposedly on the disk, but really only mocked.'


def test_block_persistence(block):
    block.persist()
    assert len(block.persist_to_disk.call_args_list) > 0
    args, kwargs = block.persist_to_disk.call_args_list[0]
    assert args[0] == block.type + block.data
    str_path = str(args[1])
    assert block.multihash in str_path


def test_block_parse_payload(block_payload_type_X):
    block = Block.parse_payload(block_payload_type_X)
    assert block.type == b'X', block.type
    assert block.data == b'DATA', block.data


def test_block_repr(block):
    r = repr(block)
    assert 'Block' in r
    assert block.multihash in r
