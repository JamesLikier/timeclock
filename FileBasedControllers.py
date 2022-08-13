import lib.timeclock as timeclock
from lib.timeclock import Employee, Punch
import string
import time

class FileBasedEmployeeController(timeclock.EmployeeController):
    def __init__(self, filename: string):
        super().__init__(self)
        self.filename = filename

    def createEmployee(self, fname: string, lname: string, admin: bool) -> Employee:
        pass

    def getEmployeeById(self, employeeId: int) -> Employee:
        pass

    def modifyEmployee(self, employee: Employee) -> Employee:
        pass
    
class FileBasedPunchController(timeclock.PunchController):
    def __init__(self, filename: string):
        super().__init__(self)
        self.filename = filename

    def createPunch(self,
                    employeeId: int,
                    datetime: time.struct_time,
                    createdByEmployeeId: int) -> Punch:
        pass

    def getPunchById(self, punchId: int) -> Punch:
        pass

    def getPunchesByEmployeeId(self,
                            employeeId: int,
                            startDatetime: time.struct_time,
                            endDatetime: time.struct_time) -> list[Punch]:
        pass

    def modifyPunch(self, punch: Punch) -> Punch:
        pass

    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        pass

class FileBasedAuthController(timeclock.AuthController):
    def __init__(self, filename: string):
        super().__init__(self)
        self.filename = filename
 