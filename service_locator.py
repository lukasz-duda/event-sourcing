from bus import Bus
from fake_bus import FakeBus

class ServiceLocator:

    bus: Bus = FakeBus()