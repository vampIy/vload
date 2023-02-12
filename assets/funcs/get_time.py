import datetime
import time

def get_time():
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return date