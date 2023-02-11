import os
import sys
import subprocess
import json
import time
from concurrent.futures import ThreadPoolExecutor

from assets.funcs.pps import get_packets_per_second
from assets.funcs.bps import get_megabits_per_second
from assets.funcs.rps import get_ram_per_second
from assets.funcs.cps import get_cpu_per_second

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
            rps_future = executor.submit(get_ram_per_second)
            cps_future = executor.submit(get_cpu_per_second)

            mbps = mbps_future.result()
            pps = pps_future.result()
            rps = rps_future.result()
            cps = cps_future.result()

            clear()
            print(f"IP: {ip}\nPort: {port}\nType: {type}\nMegabits/s: {mbps}\nPackets/s: {pps:,}\nCpu/s: {cps}%\nRam/s: {rps}%")
            time.sleep(1)

if __name__ == '__main__':
    main()