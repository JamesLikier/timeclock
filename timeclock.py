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
    hours: float = None
    state: str = None
    IN: str = "in"
    OUT: str = "out"

    def hoursDelta(self, punch: 'Punch') -> float:
        return round(((self.datetime - punch.datetime).total_seconds() / 60 / 60),2)
    
    def setHours(self, prevPunch: 'Punch') -> 'Punch':
        if prevPunch:
            self.hours = self.hoursDelta(prevPunch)
        else:
            self.hours = 0

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

    def getPunchPairsByEmployeeId(self,
                            employeeId: int,
                            startDate: dt.date,
                            endDate: dt.date,
                            padded = False):
        punchList = self.getPunchesByEmployeeId(employeeId, startDate, endDate)
        pairList: list[PunchPair] = []
        iterList = punchList
        while len(iterList) >= 2:
            p1,p2 = iterList[0],iterList[1]
            if p1.datetime.date() == p2.datetime.date():
                pairList.append(PunchPair(p1.datetime.date(),p1,p2))
                iterList = iterList[2:]
            else:
                pairList.append(PunchPair(p1.datetime.date(),p1,None))
                iterList = iterList[1:]
        if len(iterList) > 0:
            pairList.append(PunchPair(iterList[0].datetime.date(),iterList[0],None))
        if padded:
            dates = genDates(startDate,endDate)
            padList = []
            for d in dates:
                if len(pairList) > 0 and pairList[0].date == d:
                    while(len(pairList) > 0 and pairList[0].date == d):
                        padList.append(pairList.pop(0))
                else:
                    padList.append(PunchPair(d,None,None))
            pairList = padList
        return pairList

    @abstractmethod
    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        pass

    def getPunchState(self, punch: Punch):
        return Punch.IN if self.getPunchCountUpToPunch(punch) % 2 == 0 else Punch.OUT

    @abstractmethod
    def getPreviousPunch(self, punch: Punch) -> Punch:
        pass

@dataclass
class PunchPair():
    date: dt.date = None
    p1: Punch = None
    p2: Punch = None

def genDates(startDate, endDate) -> list[dt.date]:
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

def convertDateStrToISO(s: str) -> str:
    m = re.match(r'([0-9]+)/([0-9]+)/([0-9]+)',s)
    if m is not None:
        return f'{m.group(3)}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}'
    return None

def convertTimeStrToISO(s: str) -> str:
    m = re.match(r'([0-9]+):([0-9]+)',s)
    if m is not None:
        return f'{m.group(1).zfill(2)}:{m.group(2).zfill(2)}'