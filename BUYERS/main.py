from selenium import webdriver
from backend.entities.seller import Seller
# from backend.myTypes import SubscriptionResponse


class WhatsAppDriver:
    def __init__(self, url: str, group: list):
        self.drive = webdriver.Chrome()
        self.drive.get(url)


# WhatsAppDriver("https://google.com")
WhatsAppDriver("https://web.whatsapp.com", [])
