import os
import sys
import json
import time
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

from assets.funcs.packet_per_sec import get_packets_per_second
from assets.funcs.bytes_per_sec import get_megabits_per_second
from assets.funcs.get_ram import get_ram_percentage
from assets.funcs.get_cpu import get_cpu_percentage

def clear():
    os.system('clear')

def main() -> None:
    with open("assets/config/config.json", encoding="utf-8") as config_file:
        config = json.load(config_file)

    interface = config.get("interface")
    ip = config.get("ip")
    port = config.get("port")
    type = config.get("type")

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    ascii = f"""
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀  {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀ {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀ {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆{Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇ {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇ {Fore.RESET}
{Fore.LIGHTBLUE_EX}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁ {Fore.RESET}
    """

    clear()
    print(f"{ascii}")

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            get_ram_future = executor.submit(get_ram_percentage)
            get_cpu_future = executor.submit(get_cpu_percentage)
    
            mb = mbps_future.result()
            p = pps_future.result()
            r = get_ram_future.result()
            c = get_cpu_future.result()

            print(f"IP: {ip}")
            print(f"Port: {port}")
            print(f"Type: {type}")
            print(f"Megabits/s: {mb}")
            print(f"Packets/s: {p:,}")
            print(f"Cpu: {c}%")
            print(f"Ram: {r}%")
            time.sleep(0.25)
            for i in range(7):
                sys.stdout.write('\x1b[1A')

if __name__ == '__main__':
    main()