import os
import sys
import subprocess
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

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)

            mbps = mbps_future.result()
            pps = pps_future.result()

            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
            print(f"Megabits/s: {mbps}\nPackets/s: {pps:,}")

if __name__ == '__main__':
    clear()
    hide_cursor()
    main()