import sqlite3
import timeclock as tc
import datetime as dt
from jlpyutil.SQLiteHelper import SQLTransaction, SQLRequestQueue, SQLRequestor

class EmployeeController(tc.EmployeeController):
    def __init__(self, sqlRequestQueue: SQLRequestQueue):
        self.srq = sqlRequestQueue

    def createEmployee(self,
            username: str,
            fname: str,
            lname: str,
            admin: bool = False) -> tc.Employee:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                INSERT INTO employee (username, fname, lname, admin)
                VALUES (?, ?, ?, ?)
            """, (username, fname, lname, admin))
            eid = cur.lastrowid
            return eid
        r = self.srq.createRequestor()
        result = r.request(query)
        return self.getEmployeeById(result)

    def getEmployeeById(self, employeeId: int) -> tc.Employee:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT employeeid, username, fname, lname, admin
                FROM employee
                WHERE employeeid = ?
            """, (employeeId,))
            return cur.fetchone()
        r = self.srq.createRequestor()
        result = r.request(query)
        if result:
            e = tc.Employee(
                id=result[0],
                username=result[1],
                fname=result[2],
                lname=result[3],
                admin=(result[4]==1)
            )
            return e
        else:
            return None

    def getEmployeeList(self, offset: int = 0, count: int = 0, sortBy: str = None) -> list[tc.Employee]:
        sortField = "employeeid"
        if sortBy == "fname":
            sortField = "fname"
        elif sortBy == "lname":
            sortField = "lname"
        
        selectALL = f"""
            SELECT employeeid, username, fname, lname, admin
            FROM employee
            ORDER BY {sortField}
        """
        selectCount = f"""
            SELECT employeeid, username, fname, lname, admin
            FROM employee
            ORDER BY {sortField}
            LIMIT ?
            OFFSET ?
        """
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            if count > 0:
                cur.execute(selectCount,(count,offset))
            else:
                cur.execute(selectALL)
            return cur.fetchall()
        r = self.srq.createRequestor()
        result = r.request(query)
        eList = []
        for row in result:
            eList.append(tc.Employee(id=row[0],username=row[1],fname=row[2],lname=row[3],admin=row[4]))
        return eList

    def modifyEmployee(self, employee: tc.Employee) -> tc.Employee:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                UPDATE employee
                SET username = ?, fname = ?, lname = ?, admin = ?
                WHERE employeeid = ?
            """,(employee.username,employee.fname,employee.lname,employee.admin,employee.id))
        r = self.srq.createRequestor()
        r.request(query)
        return self.getEmployeeById(employeeId=employee.id)
    
    def getEmployeeCount(self) -> int:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT count(employeeid)
                FROM employee
            """)
            return cur.fetchone()
        r = self.srq.createRequestor()
        result = r.request(query)
        return result[0]

class PunchController(tc.PunchController):
    def __init__(self, sqlRequestQueue: SQLRequestQueue, minHoursForBreak: float = 0, breakMinutes: float = 0):
        self.srq = sqlRequestQueue
        self.minHoursForBreak = minHoursForBreak
        self.breakMinutes = breakMinutes

    def createPunch(self,
            employeeId: int,
            datetime: dt.datetime = None,
            createdByEmployeeId: int = None) -> tc.Punch:
        datetime = datetime or dt.datetime.now()
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                INSERT INTO punch (employeeid, punchdatetime, createdbyemployeeid)
                VALUES (?, ?, ?)
            """,(employeeId, datetime, createdByEmployeeId or employeeId))
            return cur.lastrowid
        r = self.srq.createRequestor()
        result = r.request(query)
        return self.getPunchById(result)
    
    def deletePunchById(self, punchId: int):
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                DELETE FROM punch
                WHERE punchid = ?
            """,(punchId,))
        r = self.srq.createRequestor()
        r.request(query)

    def getPunchById(self, punchId: int) -> tc.Punch:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT punchid, employeeid, punchdatetime, createdbyemployeeid
                FROM punch
                WHERE punchid = ?
            """,(punchId,))
            return cur.fetchone()
        r = self.srq.createRequestor()
        row = r.request(query)
        if row:
            p = tc.Punch(
                id=row[0],
                employeeId=row[1],
                datetime=dt.datetime.fromisoformat(row[2]),
                createdByEmployeeId=row[3],
            )
            p.setHours(self.getPreviousPunch(p),minHoursForBreak=self.minHoursForBreak,breakMinutes=self.breakMinutes)
            p.state = self.getPunchState(p)
            return p
        else:
            return None

    def getPunchesByEmployeeId(self, 
            employeeId: int,
            startDate: dt.date,
            endDate: dt.date) -> list[tc.Punch]:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT punchid, employeeid, punchdatetime, createdbyemployeeid
                FROM punch
                WHERE employeeid = ? AND punchdatetime < date(?,"+1 days") AND punchdatetime >= ?
                ORDER BY punchdatetime
            """,(employeeId,endDate,startDate))
            return cur.fetchall()
        r = self.srq.createRequestor()
        result = r.request(query)
        pList = []
        for row in result:
            pList.append(tc.Punch(id=row[0],employeeId=row[1],datetime=dt.datetime.fromisoformat(row[2]),createdByEmployeeId=row[3]))
        #generate punchstate for each punch
        if len(pList) > 0:
            state = self.getPunchState(pList[0])
            for p in pList:
                p: tc.Punch
                p.state = state
                state = tc.Punch.IN if state == tc.Punch.OUT else tc.Punch.OUT
        #generate hours for clockouts
        if len(pList) > 0:
            prevPunch = self.getPreviousPunch(pList[0])
            for p in pList:
                if p.state == tc.Punch.OUT:
                    p.setHours(prevPunch,minHoursForBreak=self.minHoursForBreak,breakMinutes=self.breakMinutes)
                else:
                    p.hours = 0
                prevPunch = p
        return pList

    def getPunchCountUpToPunch(self, punch: tc.Punch) -> int:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT count(punchid)
                FROM punch
                WHERE employeeid = ? AND punchdatetime < ?
                ORDER BY punchdatetime
            """,(punch.employeeId,punch.datetime))
            return cur.fetchone()
        r = self.srq.createRequestor()
        result = r.request(query)
        return result[0]

    def getPreviousPunch(self, punch: tc.Punch) -> tc.Punch:
        @SQLTransaction
        def query(cur: sqlite3.Cursor):
            cur.execute("""
                SELECT punchid
                FROM punch
                WHERE employeeid = ? AND punchdatetime < ?
                ORDER BY punchdatetime DESC
                LIMIT 1
            """,(punch.employeeId, punch.datetime))
            return cur.fetchone()
        r = self.srq.createRequestor()
        row = r.request(query)
        if row:
            return self.getPunchById(row[0])
        return None

def createTables(sr: SQLRequestor):
    script = ""
    with open("create_database.sql","r") as f:
        script = f.read()
    @SQLTransaction
    def query(cur: sqlite3.Cursor):
        cur.executescript(script)
    sr.request(query)
