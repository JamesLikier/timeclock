from abc import ABC, abstractmethod
import string
from dataclasses import dataclass, field
import time

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
    def modifyEmployee(self, employee: Employee) -> Employee:
        pass

class PunchController(ABC):
    pass

class AuthController(ABC):
    pass

class TimeClock:
    def __init__(self, 
                employeeController: EmployeeController,
                punchController: PunchController,
                authController: AuthController):
        pass
    pass
