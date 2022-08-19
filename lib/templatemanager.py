from collections import defaultdict
import os
import threading
import time

class TemplateManager():
    def __init__(self, basedir=".", verbose=True):
        self.basedir = basedir
        self.verbose = verbose
        self.templates = dict()
        self.modifiedTimes = defaultdict(float)
        self.running = False
        self.thread = None
    
    def scan(self, dir=None):
        dir = dir if dir != None else self.basedir
        with os.scandir(dir) as it:
            for entry in it:
                if entry.is_file():
                    eStat = entry.stat()
                    name = entry.name.replace('.html','')
                    if eStat.st_mtime > self.modifiedTimes[name]:
                        self.modifiedTimes[name] = eStat.st_mtime
                        with open(entry.path,'rb') as file:
                            self.templates[name] = file.read()
                            if self.verbose:
                                print(f'Updating template: {name}')
                if entry.is_dir():
                    self.scan(dir=entry.path)

    def loop(self):
        while self.running:
            self.scan()
            time.sleep(5)

    def start(self):
        if self.running: return

        self.running = True
        self.thread = threading.Thread(target=TemplateManager.loop,args=(self,),daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    tm = TemplateManager("templates")
    tm.start()
    i = input()
    tm.stop()
    tm.thread.join()
    