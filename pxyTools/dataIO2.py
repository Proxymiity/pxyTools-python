import json
from pathlib import Path


def _is_json_serializable(o):
    try:
        json.dumps(o)
        return True
    except (TypeError, OverflowError):
        return False


class JSONDict(dict):
    def __init__(self, path, encoding='utf-8', data=None, test_json=True):
        self.path = Path(path)
        self.encoding = encoding
        self.test_json = test_json
        if data:
            j = data
        elif self.path.is_file():
            with open(self.path, encoding=self.encoding, mode="r") as f:
                j = json.load(f)
        else:
            j = {}
        super().__init__(j)

    def save(self):
        if self.test_json:
            if not _is_json_serializable(self):
                raise ValueError("JSON Serialization Error")
        with open(self.path, encoding=self.encoding, mode="w") as f:
            json.dump(self, f, indent=4, separators=(',', ': '))

    def reload(self):
        self.__init__(self.path, self.encoding)

    def graceful_reload(self):
        for k in self.copy():
            self.pop(k)
        if self.path.is_file():
            with open(self.path, encoding=self.encoding, mode="r") as f:
                j = json.load(f)
        else:
            j = {}
        for k, v in j.items():
            self[k] = v


class JSONList(list):
    def __init__(self, path, encoding='utf-8', data=None, test_json=True):
        self.path = Path(path)
        self.encoding = encoding
        self.test_json = test_json
        if data:
            j = data
        elif self.path.is_file():
            with open(self.path, encoding=self.encoding, mode="r") as f:
                j = json.load(f)
        else:
            j = []
        super().__init__(j)

    def save(self):
        if self.test_json:
            if not _is_json_serializable(self):
                raise ValueError("JSON Serialization Error")
        with open(self.path, encoding=self.encoding, mode="w") as f:
            json.dump(self, f, indent=4, separators=(',', ': '))

    def reload(self):
        self.__init__(self.path, self.encoding)

    def graceful_reload(self):
        for v in self.copy():
            self.remove(v)
        if self.path.is_file():
            with open(self.path, encoding=self.encoding, mode="r") as f:
                j = json.load(f)
        else:
            j = []
        for v in j:
            self.append(v)
