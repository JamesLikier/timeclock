import unittest
import FileBasedControllers as fbc
import os
import lib.timeclock as tc

class TestFileBasedEmployeeController(unittest.TestCase):

    def setUp(self):
        try:
            os.remove("employeetestfile")
        except Exception:
            pass
        self.ec = fbc.FileBasedEmployeeController("employeetestfile")

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
    def test_createPunch(self):
        pass

    def test_getPunchById(self):
        pass
    
    def test_getPunchesByEmployeeId(self):
        pass
    
    def test_modifyPunch(self):
        pass

    def test_getPunchCountUpToPunch(self):
        pass

if __name__ == "__main__":
    unittest.main()