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

            ascii_art1 = f'''
            \x1b[38;5;42m /$$    /$$\x1b[38;5;43m /$$      \x1b[38;5;44m  /$$$$$$ \x1b[38;5;45m  /$$$$$$ \x1b[38;5;51m /$$$$$$$ 
            \x1b[38;5;42m| $$   | $$\x1b[38;5;43m| $$      \x1b[38;5;44m /$$__  $$\x1b[38;5;45m /$$__  $$\x1b[38;5;51m| $$__  $$
            \x1b[38;5;42m| $$   | $$\x1b[38;5;43m| $$      \x1b[38;5;44m| $$  \ $$\x1b[38;5;45m| $$  \ $$\x1b[38;5;51m| $$  \ $$
            \x1b[38;5;42m|  $$ / $$/\x1b[38;5;43m| $$      \x1b[38;5;44m| $$  | $$\x1b[38;5;45m| $$$$$$$$\x1b[38;5;51m| $$  | $$
            \x1b[38;5;42m \  $$ $$/ \x1b[38;5;43m| $$      \x1b[38;5;44m| $$  | $$\x1b[38;5;45m| $$__  $$\x1b[38;5;51m| $$  | $$
            \x1b[38;5;42m  \  $$$/  \x1b[38;5;43m| $$      \x1b[38;5;44m| $$  | $$\x1b[38;5;45m| $$  | $$\x1b[38;5;51m| $$  | $$
            \x1b[38;5;42m   \  $/   \x1b[38;5;43m| $$$$$$$$\x1b[38;5;44m|  $$$$$$/\x1b[38;5;45m| $$  | $$\x1b[38;5;51m| $$$$$$$/
            \x1b[38;5;42m    \_/    \x1b[38;5;43m|________/\x1b[38;5;44m \______/ \x1b[38;5;45m|__/  |__/\x1b[38;5;51m|_______/ 
            ''' + print(f"Date: {t}\nIP: {ip}\nPort: {port}\nType: {type}\nMegabits/s: {mb}\nPackets/s: {p:,}\nCpu: {c}%\nRam: {r}%")
        
            ascii_art2 = f'''
            \x1b[38;5;161m /$$    /$$\x1b[38;5;162m /$$      \x1b[38;5;163m  /$$$$$$ \x1b[38;5;164m  /$$$$$$ \x1b[38;5;165m /$$$$$$$ 
            \x1b[38;5;161m| $$   | $$\x1b[38;5;162m| $$      \x1b[38;5;163m /$$__  $$\x1b[38;5;164m /$$__  $$\x1b[38;5;165m| $$__  $$
            \x1b[38;5;161m| $$   | $$\x1b[38;5;162m| $$      \x1b[38;5;163m| $$  \ $$\x1b[38;5;164m| $$  \ $$\x1b[38;5;165m| $$  \ $$
            \x1b[38;5;161m|  $$ / $$/\x1b[38;5;162m| $$      \x1b[38;5;163m| $$  | $$\x1b[38;5;164m| $$$$$$$$\x1b[38;5;165m| $$  | $$
            \x1b[38;5;161m \  $$ $$/ \x1b[38;5;162m| $$      \x1b[38;5;163m| $$  | $$\x1b[38;5;164m| $$__  $$\x1b[38;5;165m| $$  | $$
            \x1b[38;5;161m  \  $$$/  \x1b[38;5;162m| $$      \x1b[38;5;163m| $$  | $$\x1b[38;5;164m| $$  | $$\x1b[38;5;165m| $$  | $$
            \x1b[38;5;161m   \  $/   \x1b[38;5;162m| $$$$$$$$\x1b[38;5;163m|  $$$$$$/\x1b[38;5;164m| $$  | $$\x1b[38;5;165m| $$$$$$$/
            \x1b[38;5;161m    \_/    \x1b[38;5;162m|________/\x1b[38;5;163m \______/ \x1b[38;5;164m|__/  |__/\x1b[38;5;165m|_______/ 
            ''' + print(f"Date: {t}\nIP: {ip}\nPort: {port}\nType: {type}\nMegabits/s: {mb}\nPackets/s: {p:,}\nCpu: {c}%\nRam: {r}%")
            
            print(ascii_art1)
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art2)
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    main()