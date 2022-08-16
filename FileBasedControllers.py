from datetime import date
import lib.timeclock as timeclock
from lib.timeclock import Employee, EmployeeNotFound, Punch, PunchNotFound
import string
import time
import copy

class FileBasedEmployeeController(timeclock.EmployeeController):
    def __init__(self, filename: string):
        self.filename = filename
        self.nextEmployeeId = 1
        self.employeeDict = dict()

        try:
            with open(str(filename), "r") as f:
                self.nextEmployeeId = int(f.readline())
                for employeeString in f.readlines():
                    fields = employeeString.strip("\n").split(",")
                    e = Employee(id=int(fields[0]),
                                fname=fields[1],
                                lname=fields[2],
                                admin=(fields[3]=="True"))
                    self.employeeDict[e.id] = e
        except Exception:
            pass

    def exportFile(self):
        with open(str(self.filename),"w") as f:
            f.write(f"{self.nextEmployeeId}\n")
            for employee in self.employeeDict.values():
                fields = []
                fields.append(str(employee.id))
                fields.append(employee.fname)
                fields.append(employee.lname)
                fields.append(str(employee.admin))
                line = ','.join(fields) + "\n"
                f.write(line)

    def createEmployee(self, fname: string, lname: string, admin: bool) -> Employee:
        id = self.nextEmployeeId
        self.nextEmployeeId += 1

        e = Employee(id=id, fname=fname, lname=lname, admin=admin)
        self.employeeDict[id] = e

        self.exportFile()

        return copy.deepcopy(e)

    def getEmployeeById(self, employeeId: int) -> Employee:
        e = self.employeeDict.get(employeeId, None)
        if e == None:
            raise EmployeeNotFound
        return copy.deepcopy(e)
    
    def getEmployeeList(self, offset: int, count: int, sortBy: string) -> list[Employee]:
        sortFn = None
        if sortBy == "id":
            sortFn = lambda employee : employee.id
        elif sortBy == "fname":
            sortFn = lambda employee : employee.fname
        elif sortBy == "lname":
            sortFn = lambda employee : employee.lname
        
        if sortFn == None:
            return []
        if offset > len(self.employeeDict):
            return []
        if count > (len(self.employeeDict) - offset):
            count = len(self.employeeDict) - offset

        sortedList = sorted(self.employeeDict.values(),key=sortFn)
        return sortedList[offset:offset+count]

    def modifyEmployee(self, employee: Employee) -> Employee:
        if employee.id in self.employeeDict.keys():
            self.employeeDict[employee.id] = copy.deepcopy(employee)
            self.exportFile()
        else:
            raise EmployeeNotFound
        return employee
    
class FileBasedPunchController(timeclock.PunchController):
    def __init__(self, filename: string):
        self.filename = filename
        self.nextPunchId = 1
        self.punchDict = dict()
        try:
            with open(str(filename), "r") as f:
                self.nextPunchId = int(f.readline())
                for punchString in f.readlines():
                    fields = punchString.strip("\n").split(",")
                    p = Punch(int(fields[0]),int(fields[1]),time.localtime(float(fields[2])),int(fields[3]),int(fields[4]))
                    self.punchDict[p.id] = p
        except Exception:
            pass

    def exportFile(self) -> None:
        try:
            with open(str(self.filename),"w") as f:
                f.write(f"{self.nextPunchId}\n")
                for punch in self.punchDict.values():
                    punch: Punch
                    fields = []
                    fields.append(str(punch.id))
                    fields.append(str(punch.employeeId))
                    fields.append(str(time.mktime(punch.datetime)))
                    fields.append(str(punch.createdByEmployeeId))
                    fields.append(str(punch.modifiedByEmployeeId))
                    line = ",".join(fields) + "\n"
                    f.write(line)
        except Exception:
            pass

    def createPunch(self,
                    employeeId: int,
                    datetime: time.struct_time,
                    createdByEmployeeId: int) -> Punch:
        p = Punch(self.nextPunchId,employeeId=employeeId,datetime=datetime,createdByEmployeeId=createdByEmployeeId)
        self.punchDict[p.id] = p
        self.nextPunchId += 1
        self.exportFile()
        return copy.deepcopy(p)

    def getPunchById(self, punchId: int) -> Punch:
        p = self.punchDict.get(punchId,None)
        if p == None:
            raise PunchNotFound
        return copy.deepcopy(p)

    def getPunchesByEmployeeId(self,
                            employeeId: int,
                            startDatetime: time.struct_time,
                            endDatetime: time.struct_time) -> list[Punch]:
        return [copy.deepcopy(p) for p in self.punchDict.values() if p.employeeId == employeeId and time.mktime(p.datetime) > time.mktime(startDatetime) and time.mktime(p.datetime) <= time.mktime(endDatetime)]
        
    def modifyPunch(self, punch: Punch, modifiedByEmployeeId: int) -> Punch:
        pass

    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        count = 0
        for p in self.punchDict.values():
            p: Punch
            if p.employeeId == punch.employeeId and time.mktime(p.datetime) < time.mktime(punch.datetime):
                count += 1
        return count

class FileBasedAuthController(timeclock.AuthController):
    def __init__(self, filename: string):
        super().__init__(self)
        self.filename = filename
 