from collections import defaultdict
import os
import threading
import time
import re
from os import DirEntry

class CachedFileManager():
    def __init__(self, basedir=".", verbose=True, filters=None):
        self.basedir = basedir
        self.verbose = verbose
        self.files = dict()
        self.modifiedTimes = defaultdict(float)
        self.running = False
        self.thread = None
        filters = filters if filters != None else []
        self.filters = [re.compile(exp) for exp in filters]
        self.scan()

    def cacheFile(self, entry: DirEntry = None):
        if entry == None: return

        eStat = entry.stat()
        eKeyName = entry.path[len(self.basedir+'\\'):]
        if eStat.st_mtime > self.modifiedTimes[eKeyName]:
            self.modifiedTimes[eKeyName] = eStat.st_mtime
            with open(entry.path,'rb') as file:
                self.files[eKeyName] = file.read()
                if self.verbose:
                    print(f'Updating Cached File: {entry.path}')

    def scan(self, dir=None):
        dir = dir if dir != None else self.basedir
        with os.scandir(dir) as it:
            for entry in it:
                if entry.is_file():
                    if len(self.filters) > 0:
                        for f in self.filters:
                            m = f.match(entry.name)
                            if m != None:
                                self.cacheFile(entry)
                    else:
                        self.cacheFile(entry)
                if entry.is_dir():
                    self.scan(dir=entry.path)

    def loop(self, interval):
        while self.running:
            self.scan()
            time.sleep(interval)

    def start(self, interval=60):
        if self.running: return

        self.running = True
        self.thread = threading.Thread(target=cfm.loop,kwargs={"interval":interval},daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    cfm = CachedFileManager("templates")
    cfm.start(5)
    i = input()
    cfm.stop()
    cfm.thread.join()
    