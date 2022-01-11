from typing import Callable, Dict, List, Type
from bus import Bus

class FakeBus(Bus):

    __routes: Dict[Type, List[Callable]]

    def __init__(self) -> None:
        super().__init__()
        self.__routes = dict()
    
    def register_handler(self, command_type: Type, handler: Callable):
        if command_type in self.__routes:
            handlers = self.__routes[command_type]
            handlers.append(handler)
        else:
            self.__routes[command_type] = [handler]
    
    def send(self, command: any):
        command_type = type(command)
        
        if command_type not in self.__routes:
            raise Exception('No handler registered.')

        handlers = self.__routes[command_type]
        if(len(handlers) > 1):
            raise Exception('Cannot send to more than one handler.')
        
        handlers[0](command)