from datetime import datetime
from backend.myTypes import PaymentType, SubscriptionResponse
from backend.imageHandler import BankPayment
from backend.entities.owner import Owner as GroupOwner
from pony.orm import db_session
from pathlib import Path, PosixPath, WindowsPath
from backend.utils import get_current_date, MONTH, MONTH_PRICE, add_days
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

# change phone number to phonenumber class
# change expiration date to datetime
def def_seller_entity(db, orm):
    class Sellers(db.Entity):
        _table_ = 'sellers'
        phone_number = orm.PrimaryKey(str)
        id = orm.Required(int, auto=True)
        name = orm.Required(str, 30)
        active_sub = orm.Required(bool)
        sub_exp_date = orm.Required(datetime)
        sales = orm.Set('Sales')
    return Sellers


class Seller:
    @staticmethod
    def is_seller(phone_number: str) -> bool:
        return False

    @staticmethod
    @db_session()
    def register_seller(phone_number, name, SellerEntity):
        if Seller.is_seller(phone_number): raise(ValueError(f"seller with {phone_number} exist!"))
        SellerEntity(
            phone_number=phone_number,
            name=name,
            active_sub=False,
            sub_exp_date= datetime(1999,1,1,0,0,0)
        )

    def __init__(self, phone_number) -> None:
        self.phone = phone_number
        #        search db for other params
        self.name = ""
        self.id = 1010
        self.exp_date = ""

    # update_db_expiration -> inline crUd for sqlite
    @db_session()
    def update_subscription(self):
        pass

    

#===============================================================
    # if not yet expired, give a credit, 
    # handle subscription for multiple months.

    # ignore transactions made over 29 days ago
    # enforce minimum monthly payment
    # ensure payment to right account
    # error if payment_type is unknown

    def renew_subscription(self, img_path: PosixPath|WindowsPath) -> SubscriptionResponse:
        receipt = BankPayment(img_path)
        if receipt.payment_type is PaymentType.UNKNOWN: 
            error_msg = self.alert_unknown_payment()
            return SubscriptionResponse.ERROR.message(error_msg)

        if receipt.acc_num != GroupOwner.ACCOUNT_NUMBER():
            error_msg = self.alert_wrong_account()
            return SubscriptionResponse.ERROR.message(error_msg)

        if receipt.amount_paid < MONTH_PRICE:
            error_msg = self.alert_low_payment()
            return SubscriptionResponse.ERROR.message(error_msg)

        if get_current_date() >= add_days(MONTH, receipt.date):
            error_msg = self.alert_expired_transaction()
            return SubscriptionResponse.ERROR.message(error_msg)

        days_paid = receipt.amount_paid/MONTH_PRICE*MONTH
        self.exp_date: datetime = datetime(1999,1,1,0,0,0)
        if self.exp_date > get_current_date():
            self.exp_date = add_days(days_paid, self.exp_date)
        else:  # no credit! 1 month sub
            self.exp_date = add_days(days_paid, get_current_date())
        
        self.update_subscription()
        success_msg = self.success_message()
        return SubscriptionResponse.SUCCESS.message(success_msg)

    def success_message(self) -> str:
        print(f"\nPhone number: {self.phone}, you seller ID: is {self.id}")
        print("Group Subscription registered at: ", current_date)
        print("Subscription valid for 30 days. Expires : ", self.exp_date)

    def error_message(self, error_id) -> str:
        print(f"\nPhone number: {self.phone}, seller ID: {self.id}")
        print(f"Transaction failed, error code: {error_id}")
 
    def alert_low_payment(self) -> str:
        # generate ID end with '-l'
        error_id = float('inf')
        error_msg = f"{error_id}: alert_low_payment"
        # save id and reason in database
        return self.error_message(error_id)

    def alert_unknown_payment(self) -> str:
        # generate ID end with '-u'
        error_id = float('inf')
        # save id and reason in database
        error_msg = f"{error_id}: unable to process receipt"
        return self.error_message(error_id)

    def alert_wrong_account(self) -> str:
        # generate ID end with '-a'
        error_id = float('inf')
        # save id and reason in database
        error_msg = f"{error_id}: alert_wrong_account"
        return self.error_message(error_id)

    def alert_expired_transaction(self) -> str:
        # generate ID end with '-e'
        error_id = float('inf')
        # save id and reason in database
        error_msg = f"{error_id}: alert_expired_transaction"
        return self.error_message(error_id)
