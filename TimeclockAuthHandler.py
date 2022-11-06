import sqlite3
from jlpyhttp.authhandler import AuthHandler
from jlpyutil.SQLiteHelper import SQLRequestQueue, SQLTransaction
from hashlib import pbkdf2_hmac

class TimeclockAuthHandler(AuthHandler):
    def __init__(self, srq: SQLRequestQueue = None, salt = None):
        self.srq = srq
        self.salt = salt

    def validateAuth(self, username: str, password: str) -> tuple[bool,int]:
        if self.srq is None:
            return False
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT password, employeeid
                FROM auth
                WHERE employeeid = (SELECT employeeid FROM employee WHERE username = ?)
            """,(username,))
            return cur.fetchone()
        r = self.srq.createRequestor()
        result = r.request(query)
        if result:
            storedPassword = result[0]
            eid = result[1]
            hashedPassword = pbkdf2_hmac('sha256',password.encode(),self.salt,500_000)
            if storedPassword == hashedPassword:
                return (True,eid)
        return (False,0)

    def setPassword(self, username: str, password: str) -> None:
        if self.srq is None:
            return None
        hashedPassword = pbkdf2_hmac('sha256',password.encode(),self.salt,500_000)
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                INSERT INTO auth (employeeid, password)
                VALUES ((SELECT employeeid FROM employee WHERE username = ?), ?)
                ON CONFLICT (employeeid)
                DO UPDATE SET (password) = ?
            """,(username,hashedPassword,hashedPassword))
            return None
        r = self.srq.createRequestor()
        r.request(query)