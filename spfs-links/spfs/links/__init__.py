import rsa

from . import settings
from .json import json
from spfs.block import Block
from spfs.block.exceptions import BlockNotFoundError
from spfs.objects import Object

from .exceptions import InvalidSignatureError


class Link(Object):
    def __init__(self, reference):
        self.reference = reference
        self.links = {
            'reference': self.reference,
        }

    def persist(self, identity, signature):
        self.check(identity, signature)
        self.data = signature
        return super().persist()

    def check(self, identity, signature):
        identity_block = Block.retrieve(identity)

        public_key = rsa.PublicKey.load_pkcs1(identity_block.data)
        string_to_check = f'{self.reference}'.encode('ascii')
        if not rsa.verify(string_to_check, signature, public_key):
            raise InvalidSignatureError()

    @classmethod
    def retrieve(cls, multihash):
        obj = Object.retrieve(multihash)
        signature = obj.data
        reference = obj.links['reference']
        return cls(reference)
