import json
import importlib
from re import Match
import sys
from dataclasses import dataclass, field
import reloadable
from jlpyhttp.http import Request, Response
from jlpyhttp.authhandler import AuthHandler
import bootstrap

rh = bootstrap.ROUTE_HANDLER

@dataclass
class Message():
    action: str = ""
    success: bool = False
    text: str = ""
    data: dict = field(default_factory=(lambda : dict()))

    def toJSON(self):
        return json.dumps(vars(self))

    @classmethod
    def fromJSON(cls, data: str):
        m = cls()
        jd = json.loads(data)
        m.action = jd.get("action","")
        m.text = jd.get("text","")
        m.data = jd.get("data",dict())
        return m

@rh.register(["GET"],"/api/reload$")
def reloadRoutes(resp: Response, **kwargs):
    for v in sys.modules.copy().values():
        if "reloadable" in dir(v):
            importlib.reload(v)
    
    msg = Message(action="reload",success=True)
    resp.body = msg.toJSON()
    resp.send()

@rh.register(["GET"],r"/api/resetadminpw")
def resetAdminpw(resp: Response, auth: AuthHandler, **kwargs):
    msg = Message()
    try:
        auth.setPassword("admin","admin")
        msg.success = True
    except Exception:
        msg.success = False
    resp.body = msg.toJSON()
    resp.send()