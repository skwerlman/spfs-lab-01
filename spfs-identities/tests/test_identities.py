from spfs.identities import Identity


def test_identity_creation_with_PrivateKey_object(private_key):
    identity = Identity('test identity created with PrivateKey object', private_key, {'created_with_private_key': True})

    hex_form = private_key.encode().hex()
    assert identity.private_key == hex_form
    assert identity.private_key_obj == private_key
    assert identity.data['created_with_private_key'] is True
    assert identity['created_with_private_key'] is True


def test_identity_creation_with_hexadecimal_private_key(private_key):
    hex_form = private_key.encode().hex()
    identity = Identity('test identity created with PrivateKey object', hex_form, {'created_with_private_key': True})

    assert identity.private_key == hex_form
    assert identity.private_key_obj == private_key
    assert identity.data['created_with_private_key'] is True
    assert identity['created_with_private_key'] is True


def test_identity_get_box(identity, other_public_key):
    identity.get_box(other_public_key.encode().hex())
    # TODO: implement this test


def test_identity_as_dict(identity):
    d = identity.as_dict()
    assert 'name' in d, d
    assert d['name'] == identity.name, d
    assert 'private_key' in d
    assert isinstance(d['private_key'], str)
    assert 'data' in d, d
    assert d['data']['test'] is True
