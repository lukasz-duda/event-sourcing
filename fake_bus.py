from typing import List
from bus import Bus

class CommandHandler:

    __command: type
    __handler: callable

    def __init__(self, command: type, handler: callable) -> None:
        self.__command = command
        self.__handler = handler

    @property
    def command(self):
        return self.__command

    @property
    def handler(self):
        return self.__handler

class FakeBus(Bus):

    __command_handlers: List[CommandHandler]

    def __init__(self) -> None:
        super().__init__()
        self.__command_handlers = []
    
    def register_handler(self, command: type, handler: callable):
        command_handler = CommandHandler(command, handler)
        self.__command_handlers.append(command_handler)
    
    def send(self, command: any):
        matching = [x for x in self.__command_handlers if x.command == type(command)]

        if(len(matching) == 0):
            raise Exception('No handler registered.')

        if(len(matching) > 1):
            raise Exception('Cannot send to more than one handler.')
        
        matching[0].handler(command)