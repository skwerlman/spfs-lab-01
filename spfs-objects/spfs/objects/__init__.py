from spfs import constants
from spfs.blocks import Block
from spfs.json import json


def serialize(data):
    return json.dumps(data).encode('utf-8')


def serialize_multihashes(blocks):
    return b'\n'.join([block.multihash for block in blocks])


class Object:
    def __init__(self, data, links=[]):
        self.data = data
        self.links = links

    @property
    def data_blocks(self):
        return Block.break_into_blocks(self.data)

    @property
    def links_blocks(self):
        serialized_links = serialize(self.links)
        return Block.break_into_blocks(serialized_links)

    @property
    def blocks(self):
        data_blocks_list_block = self.get_blocks_list_block(self.data_blocks)
        links_blocks_list_block = self.get_blocks_list_block(self.links_blocks)

        return [data_blocks_list_block, links_blocks_list_block]

    def get_blocks_list_block(self, blocks):
        blocks = list(blocks)
        serialized_blocks_list = serialize_multihashes(blocks)
        if len(serialized_blocks_list) <= constants.BLOCK_DATA_MAX_SIZE:
            list_block = Block(data=serialized_blocks_list, type_=b'L')

        else:
            list_block_blocks = Block.break_into_blocks(serialized_blocks_list)
            list_block = self.get_blocks_list_block(list_block_blocks)

        blocks.append(list_block)
        return blocks

    def persist_related(self):
        data_blocks, links_blocks = self.blocks
        data_master_block = data_blocks[-1]
        links_master_block = links_blocks[-1]

        master_block = Block(serialize_multihashes([data_master_block, links_master_block]))
        for blocks_group in (data_blocks, links_blocks):
            for block in blocks_group:
                block.persist()
        return master_block

    def persist(self):
        master_block = self.persist_related()
        master_block.persist()
        return master_block

    @classmethod
    def retrieve(cls, multihash):
        master_block = Block.retrieve(multihash)
        master_block_blocks_list = master_block.data.split(b'\n')
        data_block = Block.retrieve(master_block_blocks_list[0])
        links_block = Block.retrieve(master_block_blocks_list[1])

        data = Block.get_data(data_block.multihash)
        links = json.loads(Block.get_data(links_block.multihash))

        return cls(data, links)
