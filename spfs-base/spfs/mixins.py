class DictLikeMixin:
    def __init__(self, *args, **kwargs):
        self.data = {}
        super().__init__(*args, **kwargs)

    def _create_key(self, key):
        if key not in self.data:
            if key.endswith('_list'):
                self.data[key] = []
            else:
                self.data[key] = {}

    def __getitem__(self, key):
        self._create_key(key)
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
