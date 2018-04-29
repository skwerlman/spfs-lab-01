from spfs.utils import get_multihash


def test_create_wallet(wallet, username, password):
    assert wallet.data['test'] is True
    key = f'{username}:{password}'.encode('utf-8')
    assert wallet.key == get_multihash(key)


def test_open_wallet(wallet, username, password):
    opened_wallet = wallet.open(username, password, get_multihash(b'foobar'))
    assert 'test' in opened_wallet.data
    assert opened_wallet.data['test'] is True


def test_persist_wallet(wallet, username, password):
    multihash = wallet.persist()
    assert wallet.persist_as_blocks.call_count == 1
    assert multihash == get_multihash(b'foobar')
