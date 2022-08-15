from abc import ABC, abstractmethod
import string
from dataclasses import dataclass, field
import time

class EmployeeNotFound(Exception):
    pass

@dataclass
class Punch:
    id: int = -1
    employeeId: int = -1
    datetime: time.struct_time = field(default_factory=time.struct_time)
    createdByEmployeeId: int = -1
    modifiedByEmployeeId: int = -1

@dataclass
class Employee:
    id: int = -1
    fname: string = ""
    lname: string = ""
    admin: bool = False

class EmployeeController(ABC):
    @abstractmethod
    def createEmployee(self, fname: string, lname: string, admin: bool) -> Employee:
        pass

    @abstractmethod
    def getEmployeeById(self, employeeId: int) -> Employee:
        pass

    @abstractmethod
    def getEmployeeList(self, offset: int, count: int, sortBy: string) -> list[Employee]:
        pass
    
    @abstractmethod
    def modifyEmployee(self, employee: Employee) -> Employee:
        pass

class PunchController(ABC):
    @abstractmethod
    def createPunch(self,
                    employeeId: int,
                    datetime: time.struct_time,
                    createdByEmployeeId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchById(self, punchId: int) -> Punch:
        pass

    @abstractmethod
    def getPunchesByEmployeeId(self,
                            employeeId: int,
                            startDatetime: time.struct_time,
                            endDatetime: time.struct_time) -> list[Punch]:
        pass
    
    @abstractmethod
    def modifyPunch(self, punch: Punch) -> Punch:
        pass

    @abstractmethod
    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        pass

class AuthController(ABC):
    pass
