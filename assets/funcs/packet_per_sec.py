import time
import psutil

def get_packets_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    return net_io_counters_2.packets_recv - net_io_counters_1.packets_recv