import os
import sys
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

from assets.funcs.pps import *
from assets.funcs.bps import *

def clear():
    os.system('clear')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def main() -> None:
    with open("assets/config/config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    interface = config.get("interface")

    clear()
    hide_cursor()

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            rps_future = executor.submit(get_ram_per_second)
            cps_future = executor.submit(get_cpu_per_second)

            mbps = mbps_future.result()
            pps = pps_future.result()
            rps = rps.future.result()
            cps = cps.future.result()

            print(f"Megabits/s: {mbps}\nPackets/s: {pps:,}\nCpu%/s: {cps}\nRam%/s: {rps}")

if __name__ == '__main__':
    main()