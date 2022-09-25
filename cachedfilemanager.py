import os
import logging

class CachedFile():
    def __init__(self, path: str):
        self.path = path
        self.mtime = 0
        self.data = None
    
    def revalidate(self):
        try:
            statresult = os.stat(self.path)
            if self.mtime < statresult.st_mtime:
                self.mtime = statresult.st_mtime
                with open(self.path,'rb') as file:
                    logging.debug(f"Caching {self.path}")
                    self.data = file.read()
        except Exception:
            self.mtime = 0
            self.data = None
    
    def get(self):
        self.revalidate()
        return self.data

class CachedFileManager():
    def __init__(self):
        self.cache = dict()

    def get(self, *path) -> bytes:
        if len(path) > 1:
            filepath = os.path.join(*path)
        else:
            filepath, = path
        logging.debug(f"Attempting to find {filepath}")

        if(filepath not in self.cache.keys()):
            logging.debug(f"{filepath} not found in cache, attempting to add")
            self.cache[filepath] = CachedFile(filepath)
        return self.cache[filepath].get()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    cfm = CachedFileManager()
    data = cfm.get(".","templates","index.html")
    logging.debug(data)