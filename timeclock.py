from abc import ABC, abstractmethod
from collections import namedtuple
import string
from dataclasses import dataclass, field
import time

class EmployeeNotFound(Exception):
    pass

class PunchNotFound(Exception):
    pass

daysofweek = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
@dataclass
class Punch:
    id: int = -1
    employeeId: int = -1
    ftime: float = field(default_factory=lambda : time.time())
    createdByEmployeeId: int = -1
    modifiedByEmployeeId: int = -1

    def dateString(self):
        ts = time.localtime(self.ftime)
        return f'{ts.tm_mon}/{ts.tm_mday}/{ts.tm_year}'
    def timeString(self):
        ts = time.localtime(self.ftime)
        return f'{str(ts.tm_hour).zfill(2)}:{str(ts.tm_min).zfill(2)}'
    def dayString(self):
        ts = time.localtime(self.ftime)
        return f'{daysofweek[ts.tm_wday]}'

@dataclass
class Employee:
    id: int = -1
    fname: string = ""
    lname: string = ""
    admin: bool = False

class EmployeeController(ABC):
    @abstractmethod
    def createEmployee(self, fname: string, lname: string, admin: bool = False) -> Employee:
        pass

    @abstractmethod
    def getEmployeeById(self, employeeId: int) -> Employee:
        pass

    @abstractmethod
    def getEmployeeList(self, offset: int = 0, count: int = 0, sortBy: string = "") -> list[Employee]:
        pass
    
    @abstractmethod
    def modifyEmployee(self, employee: Employee) -> Employee:
        pass

class PunchController(ABC):
    @abstractmethod
    def createPunch(self,
                    employeeId: int,
                    ftime: float,
                    createdByEmployeeId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchById(self, punchId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchesByEmployeeId(self,
                            employeeId: int,
                            startFtime: float,
                            endFtime: float) -> list[Punch]:
        pass
    
    @abstractmethod
    def modifyPunch(self, punch: Punch, modifiedByEmployeeId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        pass

    def getPunchState(self, punch: Punch):
        return "in" if self.getPunchCountUpToPunch(punch) % 2 == 0 else "out"


class AuthController(ABC):
    pass

PunchState = namedtuple('PunchState',['punch','state'])
@dataclass
class PunchPair():
    ftime: str = None
    p1: PunchState = None
    p2: PunchState = None
def pairPunches(punches: list[Punch],startState):
    pairs = []
    pair = PunchPair()
    state = startState
    for p in punches:
        pair.ftime = pair.ftime or p.dateString()
        ps = PunchState(p,state)
        if pair.date != p.dateString():
            pairs.append(pair)
            pair = PunchPair()
            pair.date = p.dateString()
        if pair.p1 is None:
            pair.p1 = ps
        else:
            pair.p2 = ps
            pairs.append(pair)
            pair = PunchPair()
        state = 'in' if state == 'out' else 'out'
    if pair.p1 is not None:
        pairs.append(pair)
    return pairs