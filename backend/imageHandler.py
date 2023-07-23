from PIL import Image
from pytesseract import image_to_string, pytesseract
import re
from backend.myTypes import PaymentType
from pathlib import Path, PosixPath, WindowsPath 
from datetime import datetime
from backend.utils import create_date
from datetime import timedelta, datetime


class BankPayment:
    def __init__(self, img_path: PosixPath|WindowsPath):
        self.path = img_path
        self.img_text: str = self.process_image()
        self.payment_type: PaymentType = self.get_payment_type()
        self.date: datetime = self.get_date()
        self.amount_paid: float = self.get_amount_paid()
        self.acc_num: int = self.get_account_number()


    def process_image(self)->str:
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        return image_to_string(Image.open(self.path), lang="eng")

    
    def get_payment_type(self)->PaymentType:
        def isAccess(img_text): return not not re.search("Generated from AccessMore.*", img_text)
        def isGTB(img_text): return not not re.search(".*GTWorld.*", img_text)
        def isOPay(img_text): return not not re.search(".*OPay Transaction Receipt.*", img_text)
        def isZenith(img_text): return not not re.search(".*TRANSACTION RECEIPT Z ZENITH.*", img_text)

        if isAccess(self.img_text): return PaymentType.ACCESS
        if isGTB(self.img_text): return PaymentType.GTB
        if isOPay(self.img_text): return PaymentType.OPAY
        if isZenith(self.img_text): return PaymentType.ZENITH
        return PaymentType.ANY


    def get_amount_paid(self)->float:
        def get_access_amount(img_text):
            line = re.search('Transaction Amount.*', img_text).group()[20:].replace(',','')
            return float(line)

        match self.payment_type:
            case PaymentType.UNKNOWN: return 0.00
            case PaymentType.ACCESS: return get_access_amount(self.img_text)
            case _: raise ValueError("unable to parse amount")

    def get_date(self)->datetime:
        def get_access_date(img_text):
            line = re.search("Generated from AccessMore on.*", img_text).group()[29:37]
            date = line.split('/')[::-1]
            date[0] = f"20{date[0]}"
            date = [int(num) for num in date]
            return datetime(*date)

        match self.payment_type:
            case PaymentType.UNKNOWN: return datetime(1999,1,1,0,0,0)

            case PaymentType.ACCESS: return get_access_date(self.img_text)

            case _: raise ValueError("unable to parse transaction date")

    def get_account_number(self)->str:
        def get_access_account_number(img_text):
            return re.search("Beneficiary.*", img_text).group()[12:]



        match self.payment_type:
            case PaymentType.ANY: return self.payment_type
            case PaymentType.ACCESS: return get_access_account_number(self.img_text)
            case _: raise ValueError("unable to parse account number")


