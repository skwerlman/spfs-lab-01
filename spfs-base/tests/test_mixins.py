def test_dict_like_mixin_simple_key_value(dict_like_object):
    dict_like_object['key'] = 'value'
    assert 'key' in dict_like_object.data
    assert dict_like_object.data['key'] == 'value'
    assert dict_like_object['key'] == 'value'


def test_dict_like_mixin_new_list(dict_like_object):
    dict_like_object['key_list'].append(1)
    assert 'key_list' in dict_like_object.data
    assert dict_like_object.data['key_list'] == [1]
    assert dict_like_object['key_list'] == [1]


def test_dict_like_mixin_new_dict(dict_like_object):
    dict_like_object['key1']['key2'] = 'value'
    assert 'key1' in dict_like_object.data
    assert dict_like_object.data['key1'] == {'key2': 'value'}
    assert dict_like_object['key1'] == {'key2': 'value'}
