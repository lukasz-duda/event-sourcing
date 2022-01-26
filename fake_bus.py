from typing import Callable, Dict, List, Type
from bus import Bus

class FakeBus(Bus):

    __routes: Dict[Type, List[Callable]]

    def __init__(self) -> None:
        super().__init__()
        self.__routes = dict()
    
    def register_handler(self, message_type: Type, handler: Callable):
        if message_type in self.__routes:
            handlers = self.__routes[message_type]
            handlers.append(handler)
        else:
            self.__routes[message_type] = [handler]
    
    def send(self, command: any) -> None:
        message_type = type(command)
        
        if message_type not in self.__routes:
            raise Exception('No handler registered.')

        handlers = self.__routes[message_type]
        if(len(handlers) > 1):
            raise Exception('Cannot send to more than one handler.')
        
        handlers[0](command)
    
    def publish(self, event: any) -> None:
        message_type = type(event)
        
        if message_type not in self.__routes:
            return

        for handler in self.__routes[message_type]:
            handler(event)