from datetime import datetime

class Event:

    _event_type: str
    _timestamp: datetime

    def __init__(self, event_type: str, timestamp: datetime) -> None:
        self._event_type = event_type
        self._timestamp = timestamp

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def timestamp(self) -> datetime:
        return self._timestamp