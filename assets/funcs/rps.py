import psutil

def get_ram_per_second():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent