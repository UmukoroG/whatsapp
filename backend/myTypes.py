from enum import Enum, unique


@unique
class PaymentType(Enum):
    ACCESS = 1
    GTB = 2     
    OPAY = 3
    ZENITH = 4
    ANY = 5
    UNKNOWN = 6


@unique
class SubscriptionResponse(Enum):
    SUCCESS = 1
    ERROR = 2

    def __init__(self, *_):
        self.txt = ""

    def message(self, txt):
        self.txt = txt
        return self


class WhatsAppGroupConfig:
    def __init__(self):
        self.url, self.name = "", ""
