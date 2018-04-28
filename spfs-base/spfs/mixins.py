class DictLikeMixin:
    def __init__(self, *args, **kwargs):
        self.data = {}
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if key not in self.data:
            if key.endswith('_list'):
                self.data[key] = []
            else:
                self.data[key] = {}
        self.data[key] = value
