from typing import List
from bus import Bus


class FakeBus(Bus):

    __handlers: List[tuple]

    def __init__(self) -> None:
        super().__init__()
        self.__handlers = []
    
    def register_handler(self, command: type, command_handler: callable):
        self.__handlers.append((command, command_handler))
    
    def send(self, command: any):
        self.__handlers[0][1](command)