class Result:

    _success: bool
    _error: str
    _value: any

    def __init__(self, success: bool, error: str = None, value: any = None) -> None:
        self._success = success
        self._error = error if not success else None
        self._value = value if success else None

    @property
    def success(self) -> bool:
        return self._success
    
    @property
    def error(self) -> str:
        return self.error
    
    @property
    def value(self) -> any:
        return self._value

    def fail(error: str) -> 'Result':
        return Result(False, error)
    
    def ok(value: any = None) -> 'Result':
        return Result(True, None, value)