import os
from httphelper import Request, Response
from typing import Any

class SessionHandler():
    def __init__(self):
        self.sessions = dict()
        self.sessionByteSize = 32
        self.userCookie = 'userid'
        self.sessionCookie = 'sessionid'

    ##returns sessionid: str
    def createSession(self, userid: int, resp: Response = None) -> Response | str:
        sid = os.urandom(self.sessionByteSize).hex()
        self.sessions[userid] = sid
        if resp is not None:
            resp.cookies[self.userCookie] = f'{userid}; Path=/'
            resp.cookies[self.sessionCookie] = f'{sid}; Path=/'
        return resp or sid

    ##returns valid session: bool
    def validateSession(self, userid: int = None, sessionid: str = None, req: Request = None) -> Any:
        userid = userid or int(req.cookies.get(self.userCookie,'') or -1)
        sessionid = sessionid or req.cookies.get(self.sessionCookie,'')

        storedSession = self.sessions.get(userid,'')
        if storedSession == '':
            return False, None
        if storedSession == sessionid:
            return True, userid
        return False, None
    
    ##invalide session and set cookies if Response is supplied
    def invalidateSession(self, userid: int = None, req: Request = None, resp: Response = None) -> Response | None:
        userid = userid or int(req.cookies.get(self.userCookie,'') or -1)
        self.sessions[userid] = ''
        if resp is not None:
            resp.cookies[self.userCookie] = ''
            resp.cookies[self.sessionCookie] = ''
        return resp
    