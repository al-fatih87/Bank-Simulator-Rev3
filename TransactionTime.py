import datetime


def tranx_date_time():
    current_datetime = datetime.datetime.now()
    transaction_datetime = current_datetime.strftime("%d-%m-%Y %I:%M:%S %p")
    return transaction_datetime

