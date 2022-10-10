import settings
from httphelper import Request
from dataclasses import dataclass

session = settings.SESSION_HANDLER

@dataclass
class User():
    userid: int
    username: str
    admin: bool

    @classmethod
    def fromSession(cls, req: Request) -> 'User':
        valid, userid = session.validateSession(req=req)
        if valid:
            return cls.fromUserID(userid)
        return None
    
    @classmethod
    def fromUserID(cls, userid: int) -> 'User':
        try:
            employee = settings.EMPLOYEE_CONTROLLER.getEmployeeById(userid)
            return cls(userid=employee.id, username=f'{employee.lname}{employee.fname[0:1]}',admin=employee.admin)
        except Exception:
            return None
