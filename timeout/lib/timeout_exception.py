class TimeoutException(Exception):

    """
    Raised by the TimeoutThread when the execution of a function takes longer than the time specified.
    """

    def __init__(self, message: str):
        super().__init__(message)
