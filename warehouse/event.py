from datetime import datetime

class Event:

    event_type: str
    timestamp: datetime

    def __init__(self, event_type: str, timestamp: datetime) -> None:
        self.event_type = event_type
        self.timestamp = timestamp