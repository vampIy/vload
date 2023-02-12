import os
import sys
import json
import time
import datetime
from concurrent.futures import ThreadPoolExecutor

from assets.funcs.packet_per_sec import get_packets_per_second
from assets.funcs.bytes_per_sec import get_megabits_per_second
from assets.funcs.get_ram import get_ram_percentage
from assets.funcs.get_cpu import get_cpu_percentage
from assets.funcs.get_time import get_time

def clear():
    os.system('clear')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def main() -> None:
    with open("assets/config/config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    interface = config.get("interface")
    ip = config.get("ip")
    port = config.get("port")
    type = config.get("type")

    hide_cursor()

    ascii = '''
    vload version 1
    '''
    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            get_ram_future = executor.submit(get_ram_percentage)
            get_cpu_future = executor.submit(get_cpu_percentage)
            get_time_future = executor.submit(get_time)
    
            mb = mbps_future.result()
            p = pps_future.result()
            r = get_ram_future.result()
            c = get_cpu_future.result()
            t = get_time_future.result()
            
            clear()
            print(f"{ascii}")
            print(f"Date: {t}\nIP: {ip}\nPort: {port}\nType: {type}\nMegabits/s: {mb}\nPackets/s: {p:,}\nCpu: {c}%\nRam: {r}%")
            time.sleep(1)

if __name__ == '__main__':
    main()