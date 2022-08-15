import lib.timeclock as timeclock
from lib.timeclock import Employee, EmployeeNotFound, Punch
import string
import time
import copy

class FileBasedEmployeeController(timeclock.EmployeeController):
    def __init__(self, filename: string):
        self.filename = filename
        self.nextEmployeeId = 1
        self.employeeDict = dict()

    def createEmployee(self, fname: string, lname: string, admin: bool) -> Employee:
        id = self.nextEmployeeId
        self.nextEmployeeId += 1

        e = Employee(id=id, fname=fname, lname=lname, admin=admin)
        self.employeeDict[id] = e

        return copy.deepcopy(e)

    def getEmployeeById(self, employeeId: int) -> Employee:
        e = self.employeeDict.get(employeeId, None)
        if e == None:
            raise EmployeeNotFound
        return copy.deepcopy(e)

    def modifyEmployee(self, employee: Employee) -> Employee:
        if employee.id in self.employeeDict.keys():
            self.employeeDict[employee.id] = copy.deepcopy(employee)
        else:
            raise EmployeeNotFound
        return employee
    
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
 