import psutil

def get_ram_percentage():
    ram_percent = psutil.virtual_memory().percent
    return round(ram_percent)