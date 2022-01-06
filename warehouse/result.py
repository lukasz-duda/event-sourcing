class Result:

    success: bool
    error: str
    value: any

    def fail(error: str):
        result = Result()
        result.success = False
        result.error = error
        result.value = None
        return result
    
    def ok(value: any = None):
        result = Result()
        result.success = True
        result.error = None
        result.value = value
        return result