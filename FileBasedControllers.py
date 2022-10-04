from datetime import date
import timeclock as timeclock
from timeclock import Employee, EmployeeNotFound, Punch, PunchNotFound
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

    def createEmployee(self, fname: string, lname: string, admin: bool = False) -> Employee:
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
    
    def getEmployeeList(self, offset: int = 0, count: int = 0, sortBy: string = "id") -> list[Employee]:
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
        
        if count == 0: count = len(self.employeeDict)

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
                    print(punchString)
                    fields = punchString.strip("\n").split(",")
                    p = Punch(int(fields[0]),int(fields[1]),float(fields[2]),int(fields[3]),int(fields[4]))
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
                    fields.append(str(punch.ftime))
                    fields.append(str(punch.createdByEmployeeId))
                    fields.append(str(punch.modifiedByEmployeeId))
                    line = ",".join(fields) + "\n"
                    f.write(line)
        except Exception:
            pass

    def createPunch(self,
                    employeeId: int,
                    ftime: float = None,
                    createdByEmployeeId: int = None) -> Punch:
        createdByEmployeeId = createdByEmployeeId or employeeId
        ftime = ftime or time.time()
        p = Punch(self.nextPunchId,employeeId=employeeId,ftime=ftime,createdByEmployeeId=createdByEmployeeId)
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
                            startFtime: float = None,
                            endFtime: float = None) -> list[Punch]:
        twoWeeks = 60 * 60 * 24 * 7 * 2
        startFtime = startFtime or (time.time() - twoWeeks)
        endFtime = endFtime or time.time()
        return [copy.deepcopy(p) for p in self.punchDict.values() if p.employeeId == employeeId and p.ftime > startFtime and p.ftime <= endFtime]
        
    def modifyPunch(self, punch: Punch, modifiedByEmployeeId: int) -> Punch:
        self.punchDict[punch.id] = copy.deepcopy(punch)
        self.punchDict[punch.id].modifiedByEmployeeId = modifiedByEmployeeId
        self.exportFile()
        return copy.deepcopy(self.punchDict[punch.id])

    def getPunchCountUpToPunch(self, punch: Punch) -> int:
        count = 0
        for p in self.punchDict.values():
            p: Punch
            if p.employeeId == punch.employeeId and p.ftime < punch.ftime:
                count += 1
        return count

class FileBasedAuthController(timeclock.AuthController):
    def __init__(self, filename: string):
        super().__init__(self)
        self.filename = filename
 