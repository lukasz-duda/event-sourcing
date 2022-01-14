from abc import abstractclassmethod


class Bus:

    @abstractclassmethod
    def register_handler(self, action):
        pass

    @abstractclassmethod
    def send(self, command):
        pass

    @abstractclassmethod
    def publish(self, event):
        pass