from spfs.objects import Object

from .feed import Feed


class FeedManager:
    def __init__(self, identity):
        self.identity = identity
        self.feeds = {}

        self.retrieve()

    def retrieve(self):
        for name, feed in self.identity['feeds'].items():
            root_multihash, leaf_multihash = feed

            leaf = Object.retrieve(leaf_multihash)
            root_base = Object.retrieve(root_multihash)
            root = Feed(self, root_base, leaf)
            self.feeds[name] = root

    def create(self, name, extra_data=None, extra_links=None):
        extra_data = extra_data or {}
        extra_links = extra_links or {}

        if name in self.feeds:
            raise KeyError('Another feed with that same name already exists!')

        data = {}
        data.update(extra_data)
        data['name'] = name

        links = {}
        links.update(extra_links)
        links['_identity'] = self.identity.multihash

        base_object = Object(data, links)
        feed = Feed(self, base_object, None)
        self.feeds[name] = feed
        return feed

    def persist(self):
        for name, feed in self.feeds.items():
            base_object = feed.base_object
            leaf = feed.leaf

            base_object.persist()
            leaf.persist()

            self.identity['feeds'][name] = (base_object.multihash, leaf.multihash)

        self.identity.persist()
