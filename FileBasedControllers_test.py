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
        for x in range(5):
            self.ec.createEmployee("Jon","Doe",False)
        self.assertEqual(len(self.ec.employeeDict),5)

        self.ec = fbc.FileBasedEmployeeController("employeetestfile")
        self.assertEqual(len(self.ec.employeeDict),5)

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