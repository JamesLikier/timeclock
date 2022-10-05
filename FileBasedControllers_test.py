import unittest
import FileBasedControllers as fbc
import os
import timeclock as tc
import time
import datetime

class TestFileBasedEmployeeController(unittest.TestCase):

    def setUp(self):
        try:
            os.remove("employeetestfile")
        except Exception:
            pass
        self.ec = fbc.FileBasedEmployeeController("employeetestfile")
    
    def tearDown(self):
        try:
            os.remove("employeetestfile")
        except Exception:
            pass

    def test_fileSaveAndLoad(self):
        self.assertEqual(len(self.ec.employeeDict),0)
        testEmployees = []
        testEmployees.append(self.ec.createEmployee("Jon","Doe",False))
        testEmployees.append(self.ec.createEmployee("Bob","Dole",False))
        testEmployees.append(self.ec.createEmployee("Clark","Kent",True))
        testEmployees.append(self.ec.createEmployee("Bruce","Wayne",False))
        testEmployees.append(self.ec.createEmployee("Tony","Stark",True))
        self.assertEqual(len(self.ec.employeeDict),5)
        self.assertEqual(self.ec.nextEmployeeId,6)

        self.ec = fbc.FileBasedEmployeeController("employeetestfile")
        self.assertEqual(len(self.ec.employeeDict),5)
        for employee in testEmployees:
            e = self.ec.getEmployeeById(employee.id)
            self.assertEqual(e.id,employee.id)
            self.assertEqual(e.fname,employee.fname)
            self.assertEqual(e.lname,employee.lname)
            self.assertEqual(e.admin,employee.admin)
        self.assertEqual(self.ec.nextEmployeeId,6)

    def test_getEmployeeList(self):
        testEmployees = []
        testEmployees.append(self.ec.createEmployee("Jon","Doe",False))
        testEmployees.append(self.ec.createEmployee("Bob","Dole",False))
        testEmployees.append(self.ec.createEmployee("Clark","Kent",True))
        testEmployees.append(self.ec.createEmployee("Bruce","Wayne",False))
        testEmployees.append(self.ec.createEmployee("Tony","Stark",True))

        offset,count = 0,2
        results = self.ec.getEmployeeList(offset,count,"id")
        self.assertEqual(len(results),count)
        self.assertEqual(results[0], testEmployees[offset+0])
        self.assertEqual(results[1], testEmployees[offset+1])

        offset,count = 2,2
        results = self.ec.getEmployeeList(offset,count,"id")
        self.assertEqual(len(results),count)
        self.assertEqual(results[0], testEmployees[offset+0])
        self.assertEqual(results[1], testEmployees[offset+1])

        results = self.ec.getEmployeeList(0,2,"fname")
        self.assertEqual(len(results),2)
        self.assertEqual(results[0].fname,"Bob")
        self.assertEqual(results[1].fname,"Bruce")

        results = self.ec.getEmployeeList(0,2,"lname")
        self.assertEqual(len(results),2)
        self.assertEqual(results[0].lname,"Doe")
        self.assertEqual(results[1].lname,"Dole")

        results = self.ec.getEmployeeList(10,5,"id")
        self.assertEqual(len(results),0)

        results = self.ec.getEmployeeList(0,10,"id")
        self.assertEqual(len(results),5)

        results = self.ec.getEmployeeList(2,10,"id")
        self.assertEqual(len(results),3)

        results = self.ec.getEmployeeList(0,5,"invalid")
        self.assertEqual(len(results),0)
        
    def test_createEmployee(self):
        e = self.ec.createEmployee("Jon","Doe",False)
        self.assertEqual(e.id,1)
        self.assertEqual(e.fname, "Jon")
        self.assertEqual(e.lname, "Doe")
        self.assertEqual(e.admin, False)

        e = self.ec.createEmployee("Bob","Dole",True)
        self.assertEqual(e.id,2)
        self.assertEqual(e.fname, "Bob")
        self.assertEqual(e.lname, "Dole")
        self.assertEqual(e.admin, True)

    def test_getEmployeeById(self):
        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,(-1,))
        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,(0,))
        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,(1,))

        self.ec.createEmployee("Jon","Doe",False)

        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,(-1,))
        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,(0,))

        e = self.ec.getEmployeeById(1)
        self.assertEqual(e.id,1)
        self.assertEqual(e.fname, "Jon")
        self.assertEqual(e.lname, "Doe")
        self.assertEqual(e.admin, False)

        self.assertRaises(tc.EmployeeNotFound,self.ec.getEmployeeById,2)

        self.ec.createEmployee("Bob","Dole",True)
        e = self.ec.getEmployeeById(2)
        self.assertEqual(e.id,2)
        self.assertEqual(e.fname, "Bob")
        self.assertEqual(e.lname, "Dole")
        self.assertEqual(e.admin, True)

    def test_modifyEmployee(self):
        e = self.ec.createEmployee("Jon","Doe",False)
        self.assertEqual(e.id,1)
        self.assertEqual(e.fname, "Jon")
        self.assertEqual(e.lname, "Doe")
        self.assertEqual(e.admin, False)

        e.fname = 'Tom'
        e.lname = 'Daniels'
        e.admin = True

        e2 = self.ec.getEmployeeById(e.id)
        self.assertEqual(e2.id,1)
        self.assertEqual(e2.fname, "Jon")
        self.assertEqual(e2.lname, "Doe")
        self.assertEqual(e2.admin, False)

        self.ec.modifyEmployee(e)
        e2 = self.ec.getEmployeeById(e.id)
        self.assertEqual(e2.id,1)
        self.assertEqual(e2.fname, "Tom")
        self.assertEqual(e2.lname, "Daniels")
        self.assertEqual(e2.admin, True)

        e.id = 3
        self.assertRaises(tc.EmployeeNotFound,self.ec.modifyEmployee,e)

class TestFileBasedPunchController(unittest.TestCase):
    def setUp(self) -> None:
        try:
            os.remove("punchtestfile")
        except Exception:
            pass
        self.pc = fbc.FileBasedPunchController("punchtestfile")

    def tearDown(self):
        try:
            os.remove("punchtestfile")
        except Exception:
            pass

    def test_fileSaveAndLoad(self):
        self.assertEqual(len(self.pc.punchDict),0)
        testPunches = []
        testPunches.append(self.pc.createPunch(1))
        testPunches.append(self.pc.createPunch(1))
        testPunches.append(self.pc.createPunch(1))
        testPunches.append(self.pc.createPunch(1))
        testPunches.append(self.pc.createPunch(1))
        self.assertEqual(len(self.pc.punchDict),5)
        self.assertEqual(self.pc.nextPunchId,6)

        self.pc = fbc.FileBasedPunchController("punchtestfile")
        self.assertEqual(len(self.pc.punchDict),5)
        self.assertEqual(self.pc.nextPunchId,6)
        for punch in testPunches:
            punch: tc.Punch
            p = self.pc.getPunchById(punch.id)
            self.assertEqual(p.id,punch.id)
            self.assertEqual(p.employeeId,punch.employeeId)
            self.assertEqual(p.datetime,punch.datetime)
            self.assertEqual(p.createdByEmployeeId,punch.createdByEmployeeId)
            self.assertEqual(p.modifiedByEmployeeId,punch.modifiedByEmployeeId)
            self.assertEqual(p,punch)

    def test_createPunch(self):
        createdTime = datetime.datetime.now()
        p = self.pc.createPunch(1,createdTime)
        self.assertEqual(p.id,1)
        self.assertEqual(p.employeeId,1)
        self.assertEqual(p.datetime,createdTime)
        self.assertEqual(p.createdByEmployeeId,1)

        createdTime = datetime.datetime.now()
        p = self.pc.createPunch(1,createdTime)
        self.assertEqual(p.id,2)
        self.assertEqual(p.employeeId,1)
        self.assertEqual(p.datetime,createdTime)
        self.assertEqual(p.createdByEmployeeId,1)

    def test_getPunchById(self):
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,-1)
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,0)
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,1)

        createdTime = datetime.datetime.now()
        p = self.pc.createPunch(1,createdTime,1)
        p2 = self.pc.getPunchById(1)
        self.assertEqual(p.id,p2.id)
        self.assertEqual(p.employeeId,p2.employeeId)
        self.assertEqual(p.datetime,p2.datetime)
        self.assertEqual(p.createdByEmployeeId,p2.createdByEmployeeId)
        self.assertEqual(p,p2)

        createdTime = datetime.datetime.now()
        p = self.pc.createPunch(2,createdTime,2)
        p2 = self.pc.getPunchById(2)
        self.assertEqual(p.id,p2.id)
        self.assertEqual(p.employeeId,p2.employeeId)
        self.assertEqual(p.datetime,p2.datetime)
        self.assertEqual(p.createdByEmployeeId,p2.createdByEmployeeId)
        self.assertEqual(p,p2)

    
    def test_getPunchesByEmployeeId(self):
        currentDatetime = datetime.datetime.now()
        delta4Weeks = datetime.timedelta(weeks=4)
        delta3Weeks = datetime.timedelta(weeks=3)
        delta2Weeks = datetime.timedelta(weeks=2)
        e1_cp = []
        e1_3wp = []
        e2_cp = []
        e2_3wp = []

        e1_cp.append(self.pc.createPunch(1,currentDatetime,1))
        e1_cp.append(self.pc.createPunch(1,currentDatetime,1))
        e1_cp.append(self.pc.createPunch(1,currentDatetime,1))
        e1_3wp.append(self.pc.createPunch(1,currentDatetime - delta3Weeks,1))
        e1_3wp.append(self.pc.createPunch(1,currentDatetime - delta3Weeks,1))

        e2_cp.append(self.pc.createPunch(2,currentDatetime,2))
        e2_cp.append(self.pc.createPunch(2,currentDatetime,2))
        e2_cp.append(self.pc.createPunch(2,currentDatetime,2))
        e2_3wp.append(self.pc.createPunch(2,currentDatetime - delta3Weeks,2))
        e2_3wp.append(self.pc.createPunch(2,currentDatetime - delta3Weeks,2))

        results = self.pc.getPunchesByEmployeeId(1,currentDatetime - delta4Weeks,currentDatetime)
        self.assertEqual(len(results),5)
        for punch in results:
            punch: tc.Punch
            self.assertEqual(punch.employeeId,1)
            self.assertEqual((punch in e1_cp) or (punch in e1_3wp),True)
        results = self.pc.getPunchesByEmployeeId(2,currentDatetime - delta2Weeks,currentDatetime)
        self.assertEqual(len(results),3)
        for punch in results:
            punch: tc.Punch
            self.assertEqual(punch.employeeId,2)
            self.assertEqual((punch in e2_cp),True)
    
    def test_modifyPunch(self):
        t = time.time()
        p = self.pc.createPunch(1,t,1)
        self.assertEqual(p.id,1)
        self.assertEqual(p.employeeId,1)
        self.assertEqual(p.datetime,t)
        self.assertEqual(p.createdByEmployeeId,1)
        self.assertEqual(p.modifiedByEmployeeId,-1)

        t2 = time.time() - 60*60*24
        p.datetime = t2
        p2 = self.pc.modifyPunch(p,2)
        self.assertNotEqual(p,p2)
        self.assertEqual(p2.id,1)
        self.assertEqual(p2.datetime,t2)
        self.assertEqual(p2.employeeId,1)
        self.assertEqual(p2.modifiedByEmployeeId,2)


    def test_getPunchCountUpToPunch(self):
        curDatetime = datetime.datetime.now()
        p1 = self.pc.createPunch(1,curDatetime-datetime.timedelta(days=5),1)
        self.pc.createPunch(1,curDatetime-datetime.timedelta(days=4),1)
        p2 = self.pc.createPunch(1,curDatetime-datetime.timedelta(days=3),1)
        self.pc.createPunch(1,curDatetime-datetime.timedelta(days=2),1)
        p3 = self.pc.createPunch(1,curDatetime-datetime.timedelta(days=1),1)
        self.pc.createPunch(2,curDatetime-datetime.timedelta(days=5),2)
        self.pc.createPunch(2,curDatetime-datetime.timedelta(days=4),2)
        self.pc.createPunch(2,curDatetime-datetime.timedelta(days=3),2)
        self.pc.createPunch(2,curDatetime-datetime.timedelta(days=2),2)
        self.pc.createPunch(2,curDatetime-datetime.timedelta(days=1),2)

        count = self.pc.getPunchCountUpToPunch(p1)
        self.assertEqual(count,0)
        count = self.pc.getPunchCountUpToPunch(p2)
        self.assertEqual(count,2)
        count = self.pc.getPunchCountUpToPunch(p3)
        self.assertEqual(count,4)

    def test_getPunchState(self):
        p1 = self.pc.createPunch(1)
        self.assertEqual(self.pc.getPunchState(p1),'in')
        p2 = self.pc.createPunch(1)
        self.assertEqual(self.pc.getPunchState(p1),'in')
        self.assertEqual(self.pc.getPunchState(p2),'out')

        p3 = self.createPunch(2)
        p4 = self.createPunch(3)
        self.assertEqual(self.pc.getPunchState(p1),'in')
        self.assertEqual(self.pc.getPunchState(p2),'out')
        self.assertEqual(self.pc.getPunchState(p3),'in')
        self.assertEqual(self.pc.getPunchState(p4),'in')

class TestPunchPair(unittest.TestCase):
    def setUp(self) -> None:
        try:
            os.remove("punchtestfile")
        except Exception:
            pass
        self.pc = fbc.FileBasedPunchController("punchtestfile")

    def tearDown(self):
        try:
            os.remove("punchtestfile")
        except Exception:
            pass
    def test_pairPunchesSameDay(self):
        for x in range(3):
            punchin = datetime.datetime(2022,9,1,15,0) + datetime.timedelta(days=0)
            punchout = punchin + datetime.timedelta(hours=8) + datetime.timedelta(days=0)
            self.pc.createPunch(1,punchin)
            self.pc.createPunch(1,punchout)
        punchList = self.pc.getPunchesByEmployeeId(1,datetime.datetime(2022,1,1))
        self.assertEqual(len(punchList),6)
        startState = 'in' if self.pc.getPunchCountUpToPunch(punchList[0]) % 2 == 0 else 'out'
        self.assertEqual(startState,'in')
        pairList = tc.pairPunches(punchList,startState)
        self.assertEqual(len(pairList),3)
    def test_pairPunchesOffsetDay(self):
        for x in range(3):
            punchin = datetime.datetime(2022,9,1,22,0) + datetime.timedelta(days=x)
            punchout = punchin + datetime.timedelta(hours=8)
            self.pc.createPunch(1,punchin)
            self.pc.createPunch(1,punchout)
        punchList = self.pc.getPunchesByEmployeeId(1,datetime.datetime(2022,1,1))
        self.assertEqual(len(punchList),6)
        startState = 'in' if self.pc.getPunchCountUpToPunch(punchList[0]) % 2 == 0 else 'out'
        self.assertEqual(startState,'in')
        pairList = tc.pairPunches(punchList,startState)
        self.assertEqual(len(pairList),4)


if __name__ == "__main__":
    unittest.main()