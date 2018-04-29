from nacl.secret import SecretBox

from spfs.json import json
from spfs.mixins import DictLikeMixin
from spfs.objects import Object, serialize
from spfs.utils import get_multihash


class Wallet(DictLikeMixin):
    def __init__(self, data=None, key=None):
        self.data = data or {}
        self.key = key

    @staticmethod
    def get_data(multihash):  # pragma: no cover
        return Object.get_data(multihash)

    @classmethod
    def open(cls, name, password, multihash):
        key = get_multihash(f'{name}:{password}'.encode('utf-8'))
        box = SecretBox(bytes.fromhex(key))

        encrypted_data = cls.get_data(multihash)
        serialized_data = box.decrypt(encrypted_data)

        return cls(json.loads(serialized_data), key)

    @staticmethod
    def persist_as_blocks(data):  # pragma: no cover
        return Object.break_into_blocks(data)

    def persist(self):
        serialized_data = serialize(self.data)
        box = SecretBox(bytes.fromhex(self.key))
        encrypted_data = box.encrypt(serialized_data)

        multihash = self.persist_as_blocks(encrypted_data)
        return multihash
