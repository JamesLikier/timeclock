import reloadable
import json
from dataclasses import dataclass, field

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