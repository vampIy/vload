import os
import sys
import json
import time
import psutil
import re
from colorama import Fore
import subprocess
from concurrent.futures import ThreadPoolExecutor

with open("config.json", encoding="utf-8") as config_file:
    config = json.load(config_file)

    interface = config.get("interface")
    ip = config.get("ip")
    port = config.get("port")
    type = config.get("type")

def get_last_attacked_source_port():
    with open('/var/log/syslog', 'r') as f:
        log_lines = f.readlines()

    ddos_regex = r'.*SYN_RECV.*SRCPT=(\d+).*'

    for line in reversed(log_lines):
        match = re.match(ddos_regex, line)
        if match:
            attacked_src_port = match.group(1)
            return attacked_src_port
    else:
        return
    
def get_last_attacked_destination_port():
    with open('/var/log/syslog', 'r') as f:
        log_lines = f.readlines()

    ddos_regex = r'.*SYN_RECV.*DPT=(\d+).*'

    for line in reversed(log_lines):
        match = re.match(ddos_regex, line)
        if match:
            attacked_dest_port = match.group(1)
            return attacked_dest_port
    else:
        return

def get_megabits_per_second(interface: str) -> int:
    old_b = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $1}\'" % interface, shell=True)
    old_b2 = int(float(old_b.decode('utf8').rstrip()))
    time.sleep(1)
    new_b = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $1}\'" % interface, shell=True)
    new_b2 = int(float(new_b.decode('utf8').rstrip()))
    byte = (new_b2 - old_b2)
    mbps = byte / 125000
    return round(mbps)

def get_packets_per_second(interface: str) -> int:
    old_ps = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'" % interface, shell=True)
    old_ps2 = int(float(old_ps.decode('utf8').rstrip()))
    time.sleep(1)
    new_ps = subprocess.check_output('grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'' % interface, shell=True)
    new_ps2 = int(float(new_ps.decode('utf8').rstrip()))
    return round(new_ps2 - old_ps2)

def get_cpu_percentage():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

def get_ram_percentage():
    ram_percent = psutil.virtual_memory().percent
    return ram_percent

def get_server_status():
    old_ps = subprocess.check_output("grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'" % interface, shell=True)
    old_ps2 = int(float(old_ps.decode('utf8').rstrip()))
    time.sleep(1)
    new_ps = subprocess.check_output('grep %s /proc/net/dev | cut -d : -f2 | awk \'{print $2}\'' % interface, shell=True)
    new_ps2 = int(float(new_ps.decode('utf8').rstrip()))
    pps = new_ps2.packets_recv - old_ps2.packets_recv

    if int(pps) > 2500:
        load = "High"
    if int(pps) > 1000 < 2000:
        load = "Medium"
    if int(pps) > 500 < 1000:
        load = "low"
    if int(pps) > 0 < 2500:
        load = "essentially no load"

def main() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    os.system('clear')

    with ThreadPoolExecutor() as executor:
        while True:
            mbps_future = executor.submit(get_megabits_per_second, interface)
            pps_future = executor.submit(get_packets_per_second, interface)
            get_ram_future = executor.submit(get_ram_percentage)
            get_cpu_future = executor.submit(get_cpu_percentage)
            get_srcport_future = executor.submit(get_last_attacked_source_port)
            get_dstport_future = executor.submit(get_last_attacked_destination_port)
            get_servstatus_future = executor.submit(get_server_status)
    
            mb = mbps_future.result()
            p = pps_future.result()
            r = get_ram_future.result()
            c = get_cpu_future.result()
            s = get_srcport_future.result()
            d = get_dstport_future.result()
            ss = get_servstatus_future.result()

            print(f"Server Status: {ss}  |  Mbits/s: {mb}  |  Packets/s: {p}  |  Cpu: {c}%  |  Ram: {r}%")
            print(f"Last attacked source port: {s}")
            print(f"Last attacked destination port: {d}")
            for i in range(10):
                sys.stdout.write('\x1b[1A')

if __name__ == '__main__':
    main()