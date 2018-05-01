from nacl.secret import SecretBox

from spfs.blocks import Block
from spfs.json import json
from spfs.mixins import DictLikeMixin
from spfs.objects import serialize
from spfs.utils import get_multihash


class Wallet(DictLikeMixin):
    def __init__(self, data=None, key=None):
        self.data = data or {}
        self.key = key

    @staticmethod
    def get_data(multihash):  # pragma: no cover
        return Block.get_data(multihash)

    @classmethod
    def open(cls, name, password, multihash):
        key = get_multihash(f'{name}:{password}'.encode('utf-8'))
        return cls.open_with_key(key, multihash)

    @classmethod
    def open_with_key(cls, key, multihash):
        box = SecretBox(bytes.fromhex(key))

        encrypted_data = cls.get_data(multihash)
        serialized_data = box.decrypt(encrypted_data)

        return cls(json.loads(serialized_data), key)

    @staticmethod
    def persist_as_blocks(data):  # pragma: no cover
        return Block.persist_data(data)

    def persist(self):
        serialized_data = serialize(self.data)
        box = SecretBox(bytes.fromhex(self.key))
        encrypted_data = box.encrypt(serialized_data)

        return self.persist_as_blocks(encrypted_data)
