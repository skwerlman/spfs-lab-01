from nacl.secret import SecretBox

from spfs.json import json
from spfs.mixins import DictLikeMixin
from spfs.objects import Object, serialize
from spfs.utils import get_multihash


class Wallet(DictLikeMixin):
    def __init__(self, data=None, key=None):
        self.data = data or {}
        self.key = key

    @classmethod
    def open(cls, name, password, multihash):
        key = get_multihash(f'{name}:{password}')
        box = SecretBox(key)

        encrypted_data = Object.get_data(multihash)
        serialized_data = box.decrypt(encrypted_data)

        return cls(json.loads(serialized_data), key)

    def persist(self):
        serialized_data = serialize(self.data)
        box = SecretBox(self.key)
        encrypted_data = box.encrypt(serialized_data)

        multihash = Object.break_into_blocks(encrypted_data)
        return multihash
