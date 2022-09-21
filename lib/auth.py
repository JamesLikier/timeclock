class AuthHandler():
    def __init__(self):
        pass
    
    ##returns valid login info: bool
    def validateCredentials(username: str, password: str) -> bool:
        pass

    ##returns sessionid: str
    def createSession(userid: int) -> str:
        pass

    ##returns valid session: bool
    def validateSession(userid: int, sessionid: str) -> bool:
        pass