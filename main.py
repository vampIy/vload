import os
import sys
import json
import time
import psutil
import re
from colorama import Fore
import subprocess
from concurrent.futures import ThreadPoolExecutor

interface = "eth0"

def get_incomingmb_per_second(interface: str) -> int:
    net_io_counters = psutil.net_io_counters()
    bytes_recv = net_io_counters.bytes_recv
    time.sleep(1)
    net_io_counters = psutil.net_io_counters()
    bytes_recv_diff = net_io_counters.bytes_recv - bytes_recv
    inbound_mbps = bytes_recv_diff / 1e6 * 8
    return inbound_mbps

def get_outgoingmb_per_second(interface: str) -> int:
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    time.sleep(1)
    net_io_counters = psutil.net_io_counters()
    bytes_sent_diff = net_io_counters.bytes_sent - bytes_sent
    outbound_mbps = bytes_sent_diff / 1e6 * 8
    return outbound_mbps

def get_packets_per_second(interface: str) -> int:
    packets_1 = int(psutil.net_io_counters().packets_recv)
    time.sleep(1)
    packets_2 = int(psutil.net_io_counters().packets_recv)
    pps = packets_2 - packets_1
    return pps

def get_cpu_percentage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def get_ram_percentage():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent

def get_server_status():
    packets_1 = int(psutil.net_io_counters().packets_recv)
    time.sleep(1)
    packets_2 = int(psutil.net_io_counters().packets_recv)
    pps = packets_2 - packets_1

    if int(pps) > 2500:
        load = "High"
    if int(pps) > 1000 < 2000:
        load = "Medium"
    if int(pps) > 500 < 1000:
        load = "low"
    if int(pps) > 0 < 2500:
        load = "None"

    return load

def main() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    os.system('clear')

    with ThreadPoolExecutor() as executor:
        while True:
            inboundmb_future = executor.submit(get_incomingmb_per_second, interface)
            outboundmb_future = executor.submit(get_outgoingmb_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            get_ram_future = executor.submit(get_ram_percentage)
            get_cpu_future = executor.submit(get_cpu_percentage)
            get_servstatus_future = executor.submit(get_server_status)
    
            inmb = inboundmb_future.result()
            outmb = outboundmb_future.result()
            pps = pps_future.result()
            ram = get_ram_future.result()
            cpu = get_cpu_future.result()
            stat = get_servstatus_future.result()

            print(f"Server Status: {stat}")
            print(f"Packets: {pps}")
            print(f"Incoming: {inmb} Mbit/s")
            print(f"Outgoing: {outmb} Mbit/s")
            print(f"Cpu Usage: {cpu}%")
            print(f"Ram Usage: {ram}%")
            for i in range(5):
                sys.stdout.write('\x1b[1A')

if __name__ == '__main__':
    main()