import json
import threading
import time
import subprocess
import os

def clear():
    os.system('clear')

with open("assets/config/config.json", "r") as config_file:
    config = json.load(config_file)
interface = config.get("interface")

def print_bytes_per_second():
    while True:
        old_bytes1 = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $1}\'" % interface, shell=True)
        old_bytes2 = int(float(old_bytes1.decode('utf8').rstrip()))
        time.sleep(1)
        new_bytes1 = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $1}\'" % interface, shell=True)
        new_bytes2 = int(float(new_bytes1.decode('utf8').rstrip()))
        byte = (new_bytes2 - old_bytes2)
        mbps = byte / 125000
        print("\033[1;1H", end='')
        print(f"MB/s: {mbps}")
        time.sleep(0.5)