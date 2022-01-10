class Result:

    __success: bool
    __error: str
    __value: any

    def __init__(self, success: bool, error: str = None, value: any = None) -> None:
        self.__success = success
        self.__error = error if not success else None
        self.__value = value if success else None

    @property
    def success(self) -> bool:
        return self.__success
    
    @property
    def error(self) -> str:
        return self.__error
    
    @property
    def value(self) -> any:
        return self.__value

    def fail(error: str) -> 'Result':
        return Result(False, error)
    
    def ok(value: any = None) -> 'Result':
        return Result(True, None, value)