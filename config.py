import json

CONFIG_FILENAME = "app.config"
class Config():
    def __init__(self):
        self._dict = dict()

    def load(self):
        with open(CONFIG_FILENAME,"r") as f:
            self._dict = json.loads(f.read())
    
    def save(self):
        with open(CONFIG_FILENAME, "w") as f:
            f.write(json.dumps(self._dict))

    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]