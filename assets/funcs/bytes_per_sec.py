import time
import psutil

def get_megabits_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    return round((net_io_counters_2.bytes_recv - net_io_counters_1.bytes_recv) / 125000, 2)