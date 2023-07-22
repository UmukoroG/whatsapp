from PIL import Image
import pytesseract
import urllib.request
from backend.myTypes import PaymentType
from pathlib import Path, PosixPath, WindowsPath 
from datetime import datetime
from backend.utils import create_date

# create_date("1999-01-01")

class BankPayment:
    def __init__(self, img_path: PosixPath|WindowsPath):
        self.path = img_path
        # self.img_text: str = self.process_image(img_path)
        # self.payment_type: PaymentType = self.get_payment_type()
        # self.date: datetime = self.get_date()
        # self.amount_paid: float = self.get_amount_paid()
        # self.acc_num: int = self.get_account_number()

    def process_image(self, path: PosixPath|WindowsPath)->str:
        image = r'C:\Users\pauln\OneDrive\Documents\code\whatsapp\backend\img\receipts\2023\07\GTB.jpg'
        # text = pytesseract.image_to_string(Image.open(image), lang="eng")
        # text = pytesseract.image_to_string(Image.open(path), lang="eng")
        text = "text"
        print(text)
        return text
    
    def get_payment_type(self)->PaymentType:
        pass

    def get_amount_paid(self)->float:
        match self.payment_type:
            case PaymentType.ANY: return self.payment_type
            case PaymentType.GTB: return 0.00
            case _: raise ValueError("unable to parse amount")

    def get_date(self)->datetime:
        match self.payment_type:
            case PaymentType.ANY: return self.payment_type
            case _: raise ValueError("unable to parse transaction date")

    def get_account_number(self)->int:
        match self.payment_type:
            case PaymentType.ANY: return self.payment_type
            case _: raise ValueError("unable to parse account number")


image2 = r'C:\Users\pauln\OneDrive\Documents\code\whatsapp\backend\img\receipts\2023\07\GTB.jpg'
BankPayment(image2)