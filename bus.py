from abc import abstractclassmethod


class Bus:

    @abstractclassmethod
    def register_handler(self, command_handler):
        pass

    @abstractclassmethod
    def send(self, command):
        pass