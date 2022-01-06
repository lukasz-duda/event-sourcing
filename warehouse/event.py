from datetime import datetime

class Event:

    timestamp: datetime

    def __init__(self, timestamp) -> None:
        self.timestamp = timestamp