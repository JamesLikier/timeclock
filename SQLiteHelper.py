import logging
import queue
import threading
import sqlite3
from typing import Callable

##Deocrator for handling connection transactions
def SQLTransaction(func):
    def wrapper(con: sqlite3.Connection):
        cur = con.cursor()
        result = func(cur=cur)
        cur.close()
        con.commit()
        return result
    return wrapper

class SQLRequest():
    def __init__(self, query, responseQueue = None):
        self.query: Callable
        self.query = query
        self.responseQueue: queue.Queue
        self.responseQueue = responseQueue

class SQLRequestQueue():
    def __init__(self, dbFilename):
        self.dbFilename = dbFilename
        self.thread = threading.Thread(target=self.run,daemon=True)
        self.queue = queue.Queue()
    
    def run(self):
        con = sqlite3.connect(self.dbFilename)
        while True:
            try:
                req: SQLRequest
                req = self.queue.get(block=True)
                result = req.query(con)
                if req.responseQueue: req.responseQueue.put(result)
            except Exception:
                logging.error("Encountered error executing SQL Request")

    def start(self):
        self.thread.start()

    def put(self, query, respQueue = None):
        self.queue.put(SQLRequest(query,respQueue))
    
    def createRequestor(self, responseQueue: queue.Queue = None):
        return SQLRequestor(requestQueue=self, responseQueue=responseQueue)

class SQLRequestor():
    def __init__(self, requestQueue: SQLRequestQueue, responseQueue: queue.Queue = None):
        self.requestQueue = requestQueue
        self.responseQueue = responseQueue or queue.Queue()
    
    def request(self, query: Callable):
        self.requestQueue.put(query, self.responseQueue)
        return self.responseQueue.get(block=True,timeout=5)