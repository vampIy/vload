import psutil

def get_cpu_percentage():
    cpu_percent = psutil.cpu_percent()
    return round(cpu_percent)