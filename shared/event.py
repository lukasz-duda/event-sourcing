from abc import abstractclassmethod
from datetime import datetime
import uuid

class Event:

    __id: uuid.uuid4
    __event_type: str
    __timestamp: datetime

    def __init__(self, event_type: str, timestamp: datetime) -> None:
        self.__id = uuid.uuid4()
        self.__event_type = event_type
        self.__timestamp = timestamp

    @property
    def id(self) -> uuid.uuid4:
        return self.__id

    @property
    def event_type(self) -> str:
        return self.__event_type

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @abstractclassmethod
    def to_json(self) -> str:
        pass