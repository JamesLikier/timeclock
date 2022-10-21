from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
import re
import datetime as dt
import calendar as cal

class EmployeeNotFound(Exception):
    pass

class PunchNotFound(Exception):
    pass

@dataclass
class Punch:
    id: int = -1
    employeeId: int = -1
    datetime: dt.datetime = field(default_factory=lambda : dt.datetime.today())
    createdByEmployeeId: int = -1

    def hoursDelta(self, punch: 'Punch') -> float:
        return round(((self.datetime - punch.datetime).seconds / 60 / 60),2)

@dataclass
class Employee:
    id: int = -1
    username: str = ""
    fname: str = ""
    lname: str = ""
    admin: bool = False

class EmployeeController(ABC):
    @abstractmethod
    def createEmployee(self, 
            username: str,
            fname: str,
            lname: str,
            admin: bool) -> Employee:
        pass

    @abstractmethod
    def getEmployeeById(self, employeeId: int) -> Employee:
        pass

    @abstractmethod
    def getEmployeeList(self, offset: int = 0, count: int = 0, sortBy: str = "") -> list[Employee]:
        pass
    
    @abstractmethod
    def modifyEmployee(self, employee: Employee) -> Employee:
        pass

    @abstractmethod
    def getEmployeeCount(self) -> int:
        pass

class PunchController(ABC):
    @abstractmethod
    def createPunch(self,
                    employeeId: int,
                    datetime: dt.datetime,
                    createdByEmployeeId: int) -> Punch:
        pass

    @abstractmethod
    def deletePunchById(self, punchId: int):
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
    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        pass

    def getPunchState(self, punch: Punch):
        return "in" if self.getPunchCountUpToPunch(punch) % 2 == 0 else "out"

    @abstractmethod
    def getPreviousPunch(self, punch: Punch) -> Punch:
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

        #new date, so start a fresh pair
        if pair.date != p.datetime.date():
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

def genDates(startDate, endDate):
    c = cal.Calendar()
    startYear = startDate.year
    startMonth = startDate.month
    endYear = endDate.year
    endMonth = endDate.month
    result = []
    for y in range(startYear,endYear+1):
        if startYear == endYear:
            for m in range(startMonth, endMonth+1):
                if startMonth == endMonth:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m and d.day <= endDate.day and d.day >= startDate.day]
                elif m == endMonth:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m and d.day <= endDate.day]
                elif m == startMonth:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m and d.day >= startDate.day]
                else:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m]
        elif y == endYear and startYear != endYear:
            for m in range(1,endMonth+1):
                if m == endMonth:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m and d.day <= endDate.day]
                else:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m]
        elif y != endYear and y != startYear:
            for m in range(1,13):
                result += [d for d in c.itermonthdates(y,m) if d.month == m]
        elif y != endYear and y == startYear:
            for m in range(startMonth, 13):
                if m == startMonth:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m and d.day >= startDate.day]
                else:
                    result += [d for d in c.itermonthdates(y,m) if d.month == m]
    return result
def paddedPairPunches(punches: list[Punch], startState, startDate, endDate):
    pairs = pairPunches(punches, startState)
    dates = genDates(startDate, endDate)
    result = []
    for d in dates:
        if len(pairs) > 0 and pairs[0].date == d:
            while len(pairs) > 0 and pairs[0].date == d:
                result.append(pairs.pop(0))
        else:
            result.append(PunchPair(d))
    return result

def convertDateStrToISO(s: str) -> str:
    m = re.match(r'([0-9]+)/([0-9]+)/([0-9]+)',s)
    if m is not None:
        return f'{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}'
    return None

def convertTimeStrToISO(s: str) -> str:
    m = re.match(r'([0-9]+):([0-9]+)',s)
    if m is not None:
        return f'{m.group(1).zfill(2)}:{m.group(2).zfill(2)}'