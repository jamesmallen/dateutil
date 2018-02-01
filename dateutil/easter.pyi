import datetime

EASTER_JULIAN = ...  # type: int
EASTER_ORTHODOX = ...  # type: int
EASTER_WESTERN = ...  # type: int

def easter(year, method: int = ...) -> datetime.date: ...
