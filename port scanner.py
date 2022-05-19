import socket
import threading
import requests
import concurrent.futures
import time
import colorama
from colorama import *
import os
import json

colorama.init()
os.system("cls")

print(Fore.BLUE + "Open port Checker coded by" + Fore.LIGHTBLUE_EX + " @vuccinett" + Fore.CYAN)
print_lock = threading.Lock()

ip = input("enter the IP to scan: ")
port1 = int(input("enter ports(#1) [min 1]: "))
port2 = int(input("enter ports(#2) [max 65535]: "))

os.system("cls")

if port2 > 65535:
    print("Max port range is 65535!")

else:
    pass    

print(Fore.LIGHTCYAN_EX + f"Scanning from port {port1} to port {port2} \n")


def listToString(string):
    str1 = ""
    for element in string:
        str1 += element
    return str1


def scan(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        scanner.connect((ip, port))
        scanner.close()
        with print_lock:
            try:
                req1 = requests.get(f"https://api.mcsrvstat.us/2/{ip}:{port}")
                req1 = req1.text
                req1 = json.loads(req1)
                motd = req1["motd"]
                motd = motd['clean']
                motd = listToString(motd)
                players1 = req1["players"]
                players = players1["online"]
                playersmax = players1["max"]
                print(Fore.GREEN + f"[{port}] is Open!" + Fore.LIGHTBLACK_EX + f"  [SERVER]:   MOTD = {motd}" + f" ## PLAYERS = {players}/{playersmax}")
            except:
                print(Fore.GREEN + f"[{port}] is Open!")
    except:
        pass

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for port in range(port1, port2):
        executor.submit(scan, ip, port + 1)

print(Fore.RED + "\nAll port scanned!")
time.sleep(100000)
