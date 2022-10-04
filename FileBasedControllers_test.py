import unittest
import FileBasedControllers as fbc
import os
import timeclock as tc
import time

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
            self.assertEqual(p.ftime,punch.ftime)
            self.assertEqual(p.createdByEmployeeId,punch.createdByEmployeeId)
            self.assertEqual(p.modifiedByEmployeeId,punch.modifiedByEmployeeId)
            self.assertEqual(p,punch)

    def test_createPunch(self):
        createdTime = time.time()
        p = self.pc.createPunch(1,createdTime)
        self.assertEqual(p.id,1)
        self.assertEqual(p.employeeId,1)
        self.assertEqual(p.ftime,createdTime)
        self.assertEqual(p.createdByEmployeeId,1)

        time.sleep(1)
        createdTime = time.time()
        p = self.pc.createPunch(1,createdTime)
        self.assertEqual(p.id,2)
        self.assertEqual(p.employeeId,1)
        self.assertEqual(p.ftime,createdTime)
        self.assertEqual(p.createdByEmployeeId,1)

    def test_getPunchById(self):
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,-1)
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,0)
        self.assertRaises(tc.PunchNotFound,self.pc.getPunchById,1)

        createdTime = time.localtime()
        p = self.pc.createPunch(1,createdTime,1)
        p2 = self.pc.getPunchById(1)
        self.assertEqual(p.id,p2.id)
        self.assertEqual(p.employeeId,p2.employeeId)
        self.assertEqual(p.ftime,p2.ftime)
        self.assertEqual(p.createdByEmployeeId,p2.createdByEmployeeId)
        self.assertEqual(p,p2)

        time.sleep(1)
        createdTime = time.localtime()
        p = self.pc.createPunch(2,createdTime,2)
        p2 = self.pc.getPunchById(2)
        self.assertEqual(p.id,p2.id)
        self.assertEqual(p.employeeId,p2.employeeId)
        self.assertEqual(p.ftime,p2.ftime)
        self.assertEqual(p.createdByEmployeeId,p2.createdByEmployeeId)
        self.assertEqual(p,p2)

    
    def test_getPunchesByEmployeeId(self):
        currentFtime = time.time()
        fourWeeksAgo = currentFtime - (4 * 60 * 60 * 24 * 7)
        threeWeeksAgo = currentFtime - (3 * 60 * 60 * 24 * 7)
        twoWeeksAgo = currentFtime - (2 * 60 * 60 * 24 * 7)
        e1_cp = []
        e1_3wp = []
        e2_cp = []
        e2_3wp = []
        e1_cp.append(self.pc.createPunch(1,currentFtime,1))
        e1_cp.append(self.pc.createPunch(1,currentFtime,1))
        e1_cp.append(self.pc.createPunch(1,currentFtime,1))
        e1_3wp.append(self.pc.createPunch(1,threeWeeksAgo,1))
        e1_3wp.append(self.pc.createPunch(1,threeWeeksAgo,1))
        e2_cp.append(self.pc.createPunch(2,currentFtime,2))
        e2_cp.append(self.pc.createPunch(2,currentFtime,2))
        e2_cp.append(self.pc.createPunch(2,currentFtime,2))
        e2_3wp.append(self.pc.createPunch(2,threeWeeksAgo,2))
        e2_3wp.append(self.pc.createPunch(2,threeWeeksAgo,2))

        results = self.pc.getPunchesByEmployeeId(1,fourWeeksAgo,currentFtime)
        self.assertEqual(len(results),5)
        for punch in results:
            punch: tc.Punch
            self.assertEqual(punch.employeeId,1)
            self.assertEqual((punch in e1_cp) or (punch in e1_3wp),True)
        results = self.pc.getPunchesByEmployeeId(2,twoWeeksAgo,currentFtime)
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
        self.assertEqual(p.ftime,t)
        self.assertEqual(p.createdByEmployeeId,1)
        self.assertEqual(p.modifiedByEmployeeId,-1)

        t2 = time.time() - 60*60*24
        p.ftime = t2
        p2 = self.pc.modifyPunch(p,2)
        self.assertNotEqual(p,p2)
        self.assertEqual(p2.id,1)
        self.assertEqual(p2.ftime,t2)
        self.assertEqual(p2.employeeId,1)
        self.assertEqual(p2.modifiedByEmployeeId,2)


    def test_getPunchCountUpToPunch(self):
        timeInSec = time.time()
        dayInSec = 60 * 60 * 24
        p1 = self.pc.createPunch(1,timeInSec-(5*dayInSec),1)
        self.pc.createPunch(1,timeInSec-(4*dayInSec),1)
        p2 = self.pc.createPunch(1,timeInSec-(3*dayInSec),1)
        self.pc.createPunch(1,timeInSec-(2*dayInSec),1)
        p3 = self.pc.createPunch(1,timeInSec-(1*dayInSec),1)
        self.pc.createPunch(2,timeInSec-(5*dayInSec),2)
        self.pc.createPunch(2,timeInSec-(4*dayInSec),2)
        self.pc.createPunch(2,timeInSec-(3*dayInSec),2)
        self.pc.createPunch(2,timeInSec-(2*dayInSec),2)
        self.pc.createPunch(2,timeInSec-(1*dayInSec),2)

        count = self.pc.getPunchCountUpToPunch(p1)
        self.assertEqual(count,0)
        count = self.pc.getPunchCountUpToPunch(p2)
        self.assertEqual(count,2)
        count = self.pc.getPunchCountUpToPunch(p3)
        self.assertEqual(count,4)

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
            punchin = time.mktime(time.strptime(f"9 {x+26} 2022 15 0",r"%m %d %Y %H %M"))
            punchout = time.mktime(time.strptime(f"9 {x+26} 2022 23 0",r"%m %d %Y %H %M"))
            self.pc.createPunch(1,punchin)
            self.pc.createPunch(1,punchout)
        punchList = self.pc.getPunchesByEmployeeId(1)
        self.assertEqual(len(punchList),6)
        startState = 'in' if self.pc.getPunchCountUpToPunch(punchList[0]) % 2 == 0 else 'out'
        self.assertEqual(startState,'in')
        pairList = tc.pairPunches(punchList,startState)
        self.assertEqual(len(pairList),3)
    def test_pairPunchesOffsetDay(self):
        for x in range(3):
            punchin = time.strptime(f"9 {x+26} 2022 22 0",r"%m %d %Y %H %M")
            punchout = time.strptime(f"9 {x+27} 2022 6 0",r"%m %d %Y %H %M")
            self.pc.createPunch(1,punchin)
            self.pc.createPunch(1,punchout)
        punchList = self.pc.getPunchesByEmployeeId(1)
        self.assertEqual(len(punchList),6)
        startState = 'in' if self.pc.getPunchCountUpToPunch(punchList[0]) % 2 == 0 else 'out'
        self.assertEqual(startState,'in')
        pairList = tc.pairPunches(punchList,startState)
        print(f'{pairList=}')
        self.assertEqual(len(pairList),4)


if __name__ == "__main__":
    unittest.main()