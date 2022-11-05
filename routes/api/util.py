import json
import importlib
from re import Match
import sys
from dataclasses import dataclass, field
import reloadable
from jlpyhttp.http import Request, Response
from jlpyhttp.sessionhandler import SessionHandler
import settings

rh = settings.ROUTE_HANDLER

@dataclass
class Message():
    action: str = ""
    result: str = ""
    body: str = ""
    data: dict = field(default_factory=(lambda : dict()))
    SUCCESS: str = "success"
    FAIL: str = "fail"

    def toDict(self):
        return {
            "action": self.action,
            "result": self.result,
            "body": self.body,
            "data": self.data
        }
    def toJSON(self):
        return json.dumps(self.toDict())

    @classmethod
    def fromJSON(cls, data: str):
        m = cls()
        jd = json.loads(data)
        m.action = jd.get("action","")
        m.body = jd.get("body","")
        m.data = jd.get("data",dict())
        return m

@rh.register(["GET"],"/api/reload$")
def reloadRoutes(resp: Response, **kwargs):
    for v in sys.modules.copy().values():
        if "reloadable" in dir(v):
            importlib.reload(v)
    
    msg = Message(action="reload",result=Message.SUCCESS)
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["GET"],r"/api/resetadminpw")
def resetAdminpw(resp: Response, sessionHandler: SessionHandler, **kwargs):
    msg = Message()
    try:
        sessionHandler.setPassword("admin","admin")
        msg.result = msg.SUCCESS
    except Exception:
        msg.result = msg.FAIL
    resp.body = msg.toJSON()
    resp.send()