class CustomException(Exception):
    def __init__(self, status_code=500, message="Smt wrong has been occured!"):
        self.status_code = status_code
        self.message = message
        super().__init__(message)
