from abc import abstractclassmethod

class EventPublisher:

    @abstractclassmethod
    def publish(self, event):
        pass

class Bus(EventPublisher):

    @abstractclassmethod
    def register_handler(self, action):
        pass

    @abstractclassmethod
    def send(self, command):
        pass