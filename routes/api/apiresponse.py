import json
from dataclasses import dataclass, Field

@dataclass
class APIResponse():
    data: Field(default_factory=(lambda : dict()))
    action: str = ""
    result: str = ""
    body: str = ""
    SUCCESS: str = "sucess"
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