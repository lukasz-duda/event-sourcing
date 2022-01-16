from abc import abstractclassmethod

class EventPublisher:

    @abstractclassmethod
    def publish(self, event):
        pass

class CommandSender:

    @abstractclassmethod
    def send(self, command):
        pass

class Bus(EventPublisher, CommandSender):

    @abstractclassmethod
    def register_handler(self, action):
        pass