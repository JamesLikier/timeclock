import os

class AuthHandler():
    def __init__(self):
        self.sessions = dict()
        self.sessionByteSize = 32
    
    ##returns valid login info: bool
    def validateCredentials(self, username: str, password: str) -> bool:
        return True

    ##returns sessionid: str
    def createSession(self, userid: int) -> str:
        sid = os.urandom(self.sessionByteSize).hex()
        self.sessions[userid] = sid
        return sid

    ##returns valid session: bool
    def validateSession(self, userid: int, sessionid: str) -> bool:
        return len(self.sessions.get(userid, '')) > 0


if __name__ == '__main__':
    ah = AuthHandler()
    sid = ah.createSession(1)
    print(sid)
    print(ah.validateSession(1,sid))
    print(ah.validateSession(2,sid))