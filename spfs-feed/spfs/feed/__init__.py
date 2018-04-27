from spfs.objects import Object, serialize


class Feed(Object):
    def __init__(self, name, links=None):
        self.data = serialize({
            'name': name,
        })
        self.links = links or {}


class FeedEntry(Object):
    def __init__(self, data, previous=None, links=None):
        links = links or {}
        links['previous'] = previous
        super().__init__(self, data, links)
