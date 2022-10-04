from abc import ABC, abstractmethod
from collections import namedtuple
import string
from dataclasses import dataclass, field
import datetime as dt
import calendar as cal

class EmployeeNotFound(Exception):
    pass

class PunchNotFound(Exception):
    pass

daysofweek = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
@dataclass
class Punch:
    id: int = -1
    employeeId: int = -1
    datetime: dt.datetime = field(default_factory=lambda : dt.datetime.today())
    createdByEmployeeId: int = -1
    modifiedByEmployeeId: int = -1

    def dateString(self):
        dt = self.datetime
        return f'{dt.month}/{dt.day}/{dt.year}'
    def timeString(self):
        dt = self.datetime
        return f'{str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}'
    def dayString(self):
        dt = self.datetime
        return f'{daysofweek[cal.weekday(dt.year,dt.month,dt.day)]}'

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
                    datetime: dt.datetime,
                    createdByEmployeeId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchById(self, punchId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchesByEmployeeId(self,
                            employeeId: int,
                            startDate: dt.date,
                            endDate: dt.date) -> list[Punch]:
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
    date: dt.date = None
    p1: PunchState = None
    p2: PunchState = None
def pairPunches(punches: list[Punch],startState):
    pairs = []
    pair = PunchPair()
    state = startState
    for p in punches:
        pair.date = pair.date or p.datetime.date()
        ps = PunchState(p,state)
        if pair.date != p.dateString():
            pairs.append(pair)
            pair = PunchPair()
            pair.date = p.datetime.date()
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