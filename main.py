import os
import sys
import subprocess
import json
import time
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

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            rps_future = executor.submit(get_ram_percentage)
            cps_future = executor.submit(get_cpu_percentage)

            mbps = mbps_future.result()
            pps = pps_future.result()
            rps = rps_future.result()
            cps = cps_future.result()

            clear()
            print(f"Uptime: {date}\nIP: {ip}\nPort: {port}\nType: {type}\nMegabits/s: {mbps}\nPackets/s: {pps:,}\nCpu: {cps}%\nRam: {rps}%")
            time.sleep(1)

if __name__ == '__main__':
    main()