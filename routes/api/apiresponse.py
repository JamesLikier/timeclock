import json
from dataclasses import dataclass, Field

@dataclass
class APIResponse():
    data: Field(default_factory=(lambda : dict()))
    result: str = ""
    body: str = ""
