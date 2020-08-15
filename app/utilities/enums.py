from enum import Enum, unique, auto


@unique
class Pages(Enum):
    Login = auto()
    Console = auto()
    Users = auto()
    User = auto()
    Plugins = auto()
    Configs = auto()
    Login_Error = auto()
    Login_Logout = auto()
    First_Login = auto()
    Error_First_Login = auto()
    Error_No_Match_First_Login = auto()
    Invalid_User = auto()

@unique
class Loggers(Enum):
    Main = auto()
    Debug = auto()