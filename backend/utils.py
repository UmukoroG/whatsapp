from datetime import timedelta, datetime, date
# import re
from functools import wraps
from time import sleep
# from myTypes import WhatsAppGroupConfig


MONTH = 30
MONTH_PRICE = 22_000


def get_current_date():
    return datetime.today()


def add_days(day: int, date: str) -> datetime:
    return date + timedelta(days=int(day))


def delete_decimal(n: str) -> int:
    index = n.find('.')
    if index == -1:
        return int(n)
    return int(n[:index])


def create_date(date: str) -> datetime:
    return datetime.fromisoformat(date)


def function_awaited_repeat(*arg):
    func, stop = arg[0], arg[1] if len(arg) >= 2 else 5
    sleep_time = arg[2] if len(arg) >= 3 else 5 * 1000
    start = arg[3] if len(arg) >= 4 else 0

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            sleep(sleep_time)
            function_awaited_repeat(func, stop, sleep_time, start+1)() 
    if start < stop:
        return timeit_wrapper
    else: 
        raise ValueError(f"Failed {start} times. Waiting {sleep_time}s before retrys")
    
    
def problem():
    print("in probably")
    raise Exception("I am a problem")
# function_awaited_repeat(problem, 5, 1)()


# def get_whatsapp_config() -> WhatsAppGroupConfig:
#     config = WhatsAppGroupConfig
#     pass

#     with open(r'E:\data\categories.yaml') as file:
#     documents = yaml.safe_load(file)
#     for item, doc in documents.items():
#         print(item, ":", doc)
#     my_config = WhatsAppGroupConfig(url="", name="")
#     return my_config
