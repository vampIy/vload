import os
import sys
import json
import time
import psutil
import re
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

with open("config.json", encoding="utf-8") as config_file:
    config = json.load(config_file)

    interface = config.get("interface")
    ip = config.get("ip")
    port = config.get("port")
    type = config.get("type")

def get_last_attacked_source_port():
    with open('/var/log/syslog', 'r') as f:
        log_lines = f.readlines()

    ddos_regex = r'.*SYN_RECV.*SRCPT=(\d+).*'

    for line in reversed(log_lines):
        match = re.match(ddos_regex, line)
        if match:
            attacked_src_port = match.group(1)
            return attacked_src_port
    else:
        return
    
def get_last_attacked_destination_port():
    with open('/var/log/syslog', 'r') as f:
        log_lines = f.readlines()

    ddos_regex = r'.*SYN_RECV.*DPT=(\d+).*'

    for line in reversed(log_lines):
        match = re.match(ddos_regex, line)
        if match:
            attacked_dest_port = match.group(1)
            return attacked_dest_port
    else:
        return

def get_megabits_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    mbps = ((net_io_counters_2.bytes_recv - net_io_counters_1.bytes_recv) / 125000)
    return round((net_io_counters_2.bytes_recv - net_io_counters_1.bytes_recv) / 125000)

def get_packets_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    pps = net_io_counters_2.packets_recv - net_io_counters_1.packets_recv
    return net_io_counters_2.packets_recv - net_io_counters_1.packets_recv

def get_cpu_percentage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def get_ram_percentage():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent

def get_server_status():
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    pps = net_io_counters_2.packets_recv - net_io_counters_1.packets_recv
    packet_threshold = 3000

    if pps < packet_threshold:
        server_status = f"{Fore.GREEN}Excellent{Fore.RESET}"
        return server_status
    if pps <= packet_threshold:
        server_status = f"{Fore.YELLOW}Regular{Fore.RESET}"
        return server_status
    if pps > packet_threshold:
        server_status = f"{Fore.RED}Stressed{Fore.RESET}"

def main() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    ascii = f"""
    {Fore.LIGHTMAGENTA_EX}                     .::.{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}                  .:'  .:{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}        ,MMM8&&&.:'   .:'{Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}       MMMMM88&&&&  .:'  {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}      MMMMM88&&&&&&:'    {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}      MMMMM88&&&&&&      {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}    .:MMMMM88&&&&&&      {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}  .:'  MMMMM88&&&&       {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}.:'   .:'MMM8&&&'        {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}:'  .:'                  {Fore.RESET}
    {Fore.LIGHTMAGENTA_EX}'::'                     {Fore.RESET}
    """

    os.system('clear')
    print(f"{ascii}")

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            get_ram_future = executor.submit(get_ram_percentage)
            get_cpu_future = executor.submit(get_cpu_percentage)
            get_srcport_future = executor.submit(get_last_attacked_source_port)
            get_dstport_future = executor.submit(get_last_attacked_destination_port)
            get_servstatus_future = executor.submit(get_server_status)
    
            mb = mbps_future.result()
            p = pps_future.result()
            r = get_ram_future.result()
            c = get_cpu_future.result()
            s = get_srcport_future.result()
            d = get_dstport_future.result()
            ss = get_servstatus_future.result()

            print(f"Server Status: {ss}")
            print(f"IP: {ip}")
            print(f"Port: {port}")
            print(f"Type: {type}")
            print(f"Megabits/s: {mb}")
            print(f"Packets/s: {p:,}")
            print(f"Cpu(%): {c}")
            print(f"Ram(%): {r}")
            print(f"Last attacked source port: {s}")
            print(f"Last attacked destination port: {d}")
            time.sleep(0.25)
            for i in range(9):
                sys.stdout.write('\x1b[1A')

if __name__ == '__main__':
    main()