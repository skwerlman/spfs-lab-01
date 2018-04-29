import pytest

from spfs.mixins import DictLikeMixin


@pytest.fixture
def dict_like_object():
    return type('MyDictLikeClass', (DictLikeMixin,), {})()
