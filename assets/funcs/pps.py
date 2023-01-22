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

def print_packets_per_second():
    while True:
        old_packets1 = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'" % interface, shell=True)
        old_packets2 = int(float(old_packets1.decode('utf8').rstrip()))
        time.sleep(1)
        new_packets1 = subprocess.check_output('grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'' % interface, shell=True)
        new_packets2 = int(float(new_packets1.decode('utf8').rstrip()))
        pps = (new_packets2 - old_packets2)
        print("\033[2;1H", end='')
        print(f"PP/s: {pps}")
        time.sleep(0.5)