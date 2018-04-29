import re

from spfs import utils


def test_now():
    now = utils.now()
    assert re.match('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', now) is not None


def test_get_multihash():
    mh = utils.get_multihash('a'.encode('utf-8'))
    assert mh == 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'

    mh = utils.get_multihash('it is a simple test'.encode('utf-8'))
    assert mh == '032f99226ca013dd46ff749d5fa6399d88ba730152c7c94ca0f3feef1b7cac15'
