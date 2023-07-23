from datetime import datetime
import uuid
from pony import orm
from backend.myTypes import PaymentType, SubscriptionResponse
from backend.imageHandler import BankPayment
from entities.owner import Owner as GroupOwner
from pony.orm import *
from pathlib import Path, PosixPath, WindowsPath
from backend.utils import get_current_date, MONTH, MONTH_PRICE, add_days, create_date


def def_seller_entity(db):
    class Sellers(db.Entity):
        _table_ = 'sellers'
        id = orm.PrimaryKey(int, auto=True)
        phone_number = orm.Required(str, 20, unique=True)
        name = orm.Required(str, 30)
        active_sub = orm.Required(bool)
        sub_exp_date = orm.Required(str)
        last_payment_date = orm.Required(str)
        sales = orm.Set('Sales')
    return Sellers


@db_session()
def db_name(phone_number, db)->str:
    query = f"SELECT name FROM Sellers WHERE phone_number == {phone_number}"
    result = db.execute(query).fetchall()[0][0]
    return result


@db_session()
def db_id(phone_number, db):
    query = f"SELECT id FROM Sellers WHERE phone_number == {phone_number}"
    result = db.execute(query).fetchall()[0][0]
    return result


@db_session()
def db_exp_date(phone_number, db):
    query = f"SELECT sub_exp_date FROM Sellers WHERE phone_number == {phone_number}"
    result = db.execute(query).fetchall()[0][0]
    return result


class Seller:
    @staticmethod
    @db_session()
    def is_seller(phone_number: str, db) -> bool:
        query = f"SELECT id FROM Sellers WHERE phone_number=={phone_number}"
        result = db.execute(query).fetchall()
        return not not result

    @staticmethod
    @db_session()
    def register_seller(number, name, SellerEntity, db):
        if Seller.is_seller(number, db): raise(ValueError(f"seller with {number} exist!"))
        SellerEntity(
            phone_number=number,
            name=name,
            active_sub=False,
            sub_exp_date=str(datetime(1999, 1, 1, 0, 0, 0)),
            last_payment_date=str(datetime(1999, 1, 1, 0, 0, 0))
        )

    def __init__(self, phone_number, db) -> None:
        self.phone, self.db = phone_number, db
        self.name = db_name(phone_number, db)
        self.id = db_id(phone_number, db)
        self.exp_date = db_exp_date(phone_number, db)

    @db_session()
    def update_subscription(self, receipt_date):
        query = f"SELECT last_payment_date, sub_exp_date FROM Sellers WHERE phone_number=={self.phone}"
        last_payment_date, sub_exp_date = self.db.execute(query).fetchall()[0]
        if last_payment_date == str(receipt_date):
            self.exp_date = sub_exp_date
            return

        update_query = f"UPDATE Sellers SET active_sub={True}, sub_exp_date='{self.exp_date}', last_payment_date='{receipt_date}' WHERE phone_number={self.phone}"
        self.db.execute(update_query)

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

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111
        # if get_current_date() >= add_days(MONTH//2.5, receipt.date):
        if get_current_date() >= add_days(100, receipt.date):
            error_msg = self.alert_expired_transaction()
            return SubscriptionResponse.ERROR.message(error_msg)

        exp_date, days_paid = create_date(self.exp_date), receipt.amount_paid/MONTH_PRICE*MONTH
        if exp_date > get_current_date():
            self.exp_date = str(add_days(days_paid, exp_date))
        else:  # no credit! 1 month sub
            self.exp_date = str(add_days(days_paid, get_current_date()))
        self.update_subscription(receipt.date)
        success_msg = self.success_message()
        return SubscriptionResponse.SUCCESS.message(success_msg)

    def success_message(self) -> str:
        return f'''Phone number: {self.phone}, you seller ID: is {self.id}
        Group Subscription registered at: ", {get_current_date()}
        Subscription valid for 30 days. Expires : ", {self.exp_date}'''

    def error_message(self, error_id) -> str:
        return f'''Phone number: {self.phone}, seller ID: {self.id}
        Transaction failed, error code: {error_id}'''
 
    def alert_low_payment(self) -> str:
        # generate ID end with '-l'
        error_id = f"{uuid.uuid4()}-l"
        return self.error_message(error_id)

    def alert_unknown_payment(self) -> str:
        # generate ID end with '-u'
        error_id = f"{uuid.uuid4()}-u"
        return self.error_message(error_id)

    def alert_wrong_account(self) -> str:
        # generate ID end with '-a'
        error_id = f"{uuid.uuid4()}-a"
        return self.error_message(error_id)

    def alert_expired_transaction(self) -> str:
        # generate ID end with '-e'
        error_id = f"{uuid.uuid4()}-e"
        return self.error_message(error_id)
