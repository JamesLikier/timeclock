import unittest
import SQLiteControllers as sc
import timeclock as tc
import datetime as dt

class EmployeeControllerTest(unittest.TestCase):
    srq = sc.SQLRequestQueue("timeclock-test.db")
    srq.start()

    def setUp(self) -> None:
        r = EmployeeControllerTest.srq.createRequestor()
        sc.createTables(r)
        self.ec = sc.EmployeeController(EmployeeControllerTest.srq)
    
    def test_createEmployee(self):
        e = self.ec.createEmployee("bdole","bob","dole",False)
        self.assertIsNotNone(e)

    def test_getEmployee(self):
        e = self.ec.getEmployeeById(1)
        self.assertEqual(e.id,1)
        e = self.ec.getEmployeeById(2)
        self.assertIsNone(e)
        e = self.ec.createEmployee("test","test","test")
        e2 = self.ec.getEmployeeById(e.id)
        self.assertEqual(e2.id,e.id)
    
    def test_getEmployeeList(self):
        l = self.ec.getEmployeeList()
        self.assertEqual(len(l),1)
        self.ec.createEmployee("bdole","bob","dole",False)
        l = self.ec.getEmployeeList()
        self.assertEqual(len(l),2)

    def test_getEmployeeCount(self):
        c = self.ec.getEmployeeCount()
        self.assertEqual(c,1)
        self.ec.createEmployee("test","test","test")
        c = self.ec.getEmployeeCount()
        self.assertEqual(c,2)

class PunchControllerTest(unittest.TestCase):
    srq = sc.SQLRequestQueue("timeclock-test.db")
    srq.start()

    def setUp(self) -> None:
        r = PunchControllerTest.srq.createRequestor()
        sc.createTables(r)
        self.pc = sc.PunchController(PunchControllerTest.srq)
    
    def test_createPunch(self):
        p = self.pc.createPunch(1,dt.datetime.now())
        self.assertIsNotNone(p)
    
    def test_getPunch(self):
        p = self.pc.getPunchById(1)
        self.assertIsNone(p)
        p = self.pc.createPunch(1,dt.datetime.now())
        p2 = self.pc.getPunchById(p.id)
        self.assertEqual(p2.id,p.id)
    
    def test_PunchHoursState(self):
        punchDatetime = dt.datetime.now()
        p = self.pc.createPunch(1,punchDatetime)
        self.assertEqual(p.hours,0)
        self.assertEqual(p.state,tc.Punch.IN)
        p = self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        self.assertEqual(p.hours,8)
        self.assertEqual(p.state,tc.Punch.OUT)
    
    def test_getPunchList(self):
        l = self.pc.getPunchesByEmployeeId(1,dt.date.today()-dt.timedelta(weeks=2),dt.date.today())
        self.assertEqual(len(l),0)
        self.pc.createPunch(1,dt.datetime.now())
        l = self.pc.getPunchesByEmployeeId(1,dt.date.today()-dt.timedelta(weeks=2),dt.date.today())
        self.assertEqual(len(l),1)
        self.pc.createPunch(1,dt.datetime.now()-dt.timedelta(weeks=3))
        l = self.pc.getPunchesByEmployeeId(1,dt.date.today()-dt.timedelta(weeks=2),dt.date.today())
        self.assertEqual(len(l),1)

        l = self.pc.getPunchesByEmployeeId(2,dt.date.today()-dt.timedelta(weeks=2),dt.date.today())
        self.assertEqual(len(l),0)

    def test_getPunchCount(self):
        p = self.pc.createPunch(1,dt.datetime.now())
        count = self.pc.getPunchCountUpToPunch(p)
        self.assertEqual(count,0)

        p = self.pc.createPunch(1,dt.datetime.now())
        count = self.pc.getPunchCountUpToPunch(p)
        self.assertEqual(count,1)

        p2 = self.pc.createPunch(1,dt.datetime.now()+dt.timedelta(days=1))
        count = self.pc.getPunchCountUpToPunch(p)
        self.assertEqual(count,1)
        count = self.pc.getPunchCountUpToPunch(p2)
        self.assertEqual(count,2)

    def test_getPreviousPunch(self):
        p = self.pc.createPunch(1,dt.datetime.now())
        prev = self.pc.getPreviousPunch(p)
        self.assertIsNone(prev)

        p2 = self.pc.createPunch(1,dt.datetime.now())
        prev = self.pc.getPreviousPunch(p2)
        self.assertEqual(prev.id, p.id)

        p3 = self.pc.createPunch(1,dt.datetime.now())

        self.assertEqual(prev.id, p.id)

        prev = self.pc.getPreviousPunch(p3)
        self.assertEqual(prev.id, p2.id)
    
    def test_punchListStateAndHours(self):
        startDatetime = dt.datetime(2022,1,1)

        pDatetime = startDatetime
        self.pc.createPunch(1,pDatetime)
        self.pc.createPunch(1,pDatetime + dt.timedelta(hours=8))
        pl = self.pc.getPunchesByEmployeeId(1,startDatetime.date(), startDatetime.date() + dt.timedelta(days=30))
        self.assertEqual(len(pl),2)
        self.assertEqual(pl[0].hours,0)
        self.assertEqual(pl[1].hours,8)
        self.assertEqual(pl[0].state,tc.Punch.IN)
        self.assertEqual(pl[1].state,tc.Punch.OUT)

        pDatetime = pDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,pDatetime)
        self.pc.createPunch(1,pDatetime + dt.timedelta(hours=8))
        pl = self.pc.getPunchesByEmployeeId(1,startDatetime.date(), startDatetime.date() + dt.timedelta(days=30))
        self.assertEqual(len(pl),4)
        self.assertEqual(pl[0].hours,0)
        self.assertEqual(pl[1].hours,8)
        self.assertEqual(pl[2].hours,0)
        self.assertEqual(pl[3].hours,8)
        self.assertEqual(pl[2].state,tc.Punch.IN)
        self.assertEqual(pl[3].state,tc.Punch.OUT)

        pDatetime = pDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,pDatetime)
        self.pc.createPunch(1,pDatetime + dt.timedelta(hours=8))
        pl = self.pc.getPunchesByEmployeeId(1,startDatetime.date(), startDatetime.date() + dt.timedelta(days=30))
        self.assertEqual(len(pl),6)
        self.assertEqual(pl[0].hours,0)
        self.assertEqual(pl[1].hours,8)
        self.assertEqual(pl[2].hours,0)
        self.assertEqual(pl[3].hours,8)
        self.assertEqual(pl[4].hours,0)
        self.assertEqual(pl[5].hours,8)
        self.assertEqual(pl[4].state,tc.Punch.IN)
        self.assertEqual(pl[5].state,tc.Punch.OUT)
    
    def test_punchPairs(self):
        startDatetime = dt.datetime(2022,1,1)
        punchDatetime = startDatetime
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        punchDatetime = punchDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        punchDatetime = punchDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        pairList = self.pc.getPunchPairsByEmployeeId(1,startDatetime.date(),startDatetime.date()+dt.timedelta(days=30))
        self.assertEqual(len(pairList),3)
        self.assertEqual(pairList[0].date,dt.date(2022,1,1))
        self.assertEqual(pairList[0].p1.hours,0)
        self.assertEqual(pairList[0].p2.hours,8)
        self.assertEqual(pairList[1].date,dt.date(2022,1,2))
        self.assertEqual(pairList[1].p1.hours,0)
        self.assertEqual(pairList[1].p2.hours,8)
        self.assertEqual(pairList[2].date,dt.date(2022,1,3))
        self.assertEqual(pairList[2].p1.hours,0)
        self.assertEqual(pairList[2].p2.hours,8)
    
    def test_padPunchPairs(self):
        startDatetime = dt.datetime(2022,1,1)
        punchDatetime = startDatetime
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        punchDatetime = punchDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        punchDatetime = punchDatetime + dt.timedelta(days=1)
        self.pc.createPunch(1,punchDatetime)
        self.pc.createPunch(1,punchDatetime + dt.timedelta(hours=8))
        pairList = self.pc.getPunchPairsByEmployeeId(1,startDatetime.date(),startDatetime.date()+dt.timedelta(days=30),True)
        self.assertEqual(len(pairList),31)
        self.assertEqual(pairList[0].date,dt.date(2022,1,1))
        self.assertEqual(pairList[0].p1.hours,0)
        self.assertEqual(pairList[0].p2.hours,8)
        self.assertEqual(pairList[1].date,dt.date(2022,1,2))
        self.assertEqual(pairList[1].p1.hours,0)
        self.assertEqual(pairList[1].p2.hours,8)
        self.assertEqual(pairList[2].date,dt.date(2022,1,3))
        self.assertEqual(pairList[2].p1.hours,0)
        self.assertEqual(pairList[2].p2.hours,8)
        self.assertEqual(pairList[3].date,dt.date(2022,1,4))
        self.assertEqual(pairList[3].p1,None)
        self.assertEqual(pairList[3].p2,None)