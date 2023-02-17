import os
import sys
import json
import time
import psutil
import re
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

def get_last_attacked_source_port():
    with open('/var/log/syslog', 'r') as f:
        log_lines = f.readlines()

    attack_regex = r'.*SRC=.* SRCPT=(\d+)'

    for line in reversed(log_lines):
        match = re.match(attack_regex, line)
        if match:
            attacked_src_port = match.group(1)
            return attacked_src_port
    else:
        return

def get_megabits_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    return round((net_io_counters_2.bytes_recv - net_io_counters_1.bytes_recv) / 125000, 2)

def get_packets_per_second(interface: str) -> int:
    net_io_counters_1 = psutil.net_io_counters(pernic=True)[interface]
    time.sleep(1)
    net_io_counters_2 = psutil.net_io_counters(pernic=True)[interface]
    return net_io_counters_2.packets_recv - net_io_counters_1.packets_recv

def get_cpu_percentage():
    cpu_percent = psutil.cpu_percent()
    return round(cpu_percent)

def get_ram_percentage():
    ram_percent = psutil.virtual_memory().percent
    return round(ram_percent)

def main() -> None:
    with open("config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    interface = config.get("interface")
    ip = config.get("ip")
    port = config.get("port")
    type = config.get("type")

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
    
            mb = mbps_future.result()
            p = pps_future.result()
            r = get_ram_future.result()
            c = get_cpu_future.result()
            s = get_srcport_future.result()

            print(f"IP: {ip}")
            print(f"Port: {port}")
            print(f"Type: {type}")
            print(f"Megabits/s: {mb}")
            print(f"Packets/s: {p:,}")
            print(f"Cpu: {c}%")
            print(f"Ram: {r}%")
            print(f"Last attacked source port: {s}")
            time.sleep(0.25)
            for i in range(7):
                sys.stdout.write('\x1b[1A')

if __name__ == '__main__':
    main()