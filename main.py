import os
import sys
import threading
import time
import subprocess
import json

from assets.funcs.pps import *
from assets.funcs.bps import *

def clear():
    os.system('clear')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def main():
    clear()
    hide_cursor()
    threading.Thread(target=print_packets_per_second).start()
    threading.Thread(target=print_bytes_per_second).start()

if __name__ == '__main__':
    main()