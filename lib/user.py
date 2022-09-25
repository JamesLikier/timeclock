import settings
from lib.http import Request
from dataclasses import dataclass

session = settings.SESSION_HANDLER

@dataclass
class User():
    userid: int
    username: str
    admin: bool

    def fromSession(req: Request) -> 'User':
        valid, userid = session.validateSession(req=req)
        if valid:
            return User.fromUserID(userid)
        return None
    
    def fromUserID(userid: int) -> 'User':
        try:
            employee = settings.EMPLOYEE_CONTROLLER.getEmployeeById(userid)
            return User(userid=employee.id, username=f'{employee.lname}{employee.fname[0:1]}',admin=employee.admin)
        except Exception:
            return None
