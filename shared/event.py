from abc import abstractclassmethod
from datetime import datetime

class Event:

    __event_type: str
    __timestamp: datetime
    __version: int

    def __init__(self, event_type: str, timestamp: datetime) -> None:
        self.__event_type = event_type
        self.__timestamp = timestamp

    @property
    def event_type(self) -> str:
        return self.__event_type

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def version(self) -> int:
        return self.__version
    
    @version.setter
    def version(self, value: int):
        self.__version = value

    @abstractclassmethod
    def to_json(self) -> str:
        pass