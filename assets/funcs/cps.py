import psutil

def get_cpu_per_second():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent