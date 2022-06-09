import socket
import threading
import requests
import concurrent.futures
import time
import colorama
from colorama import *
import os
import json


def check():

    colorama.init()
    os.system("cls")
    banner = """ ██▓███   ▒█████   ██▀███  ▄▄▄█████▓    ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒   ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░   ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░    ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░    ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░      ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░    ░         ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
░░       ░ ░ ░ ▒    ░░   ░   ░         ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
             ░ ░     ░                 ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                       ░                       ░                               """

    print(Fore.LIGHTBLUE_EX + banner)

    print("                                                                                          coded by" + Fore.BLUE + " @vuccinett" + Fore.CYAN)
    print_lock = threading.Lock()

    ip = input("enter the IP to scan: ")
    port1 = int(input("enter ports(#1) [min 1]: "))
    port2 = int(input("enter ports(#2) [max 65535]: "))

    os.system("cls")

    if port2 > 65535:
        print(Fore.RED + "Max port range is 65535!")
        time.sleep(10)
        exit()

    elif port1 < 1:
        print(Fore.RED + "Min port range is 1!")
        time.sleep(10)
        exit()

    try:
        req = requests.get(f"https://api.mcsrvstat.us/2/{ip}")
        req = req.text
        req = json.loads(req)
        ip = req["ip"]
        print(f"Server Ip is: {ip}")
    except:
        print(Fore.RED + "You got blocked from mcsrvstats apis! restart ur wifi or change ip (Do not use VPN)")
        time.sleep(10)
        exit()

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


    try:
        req1 = requests.get(f"https://api.mcsrvstat.us/2/{ip}")
        req1 = req1.text
        req1 = json.loads(req1)
        ip = req1["ip"]
        print(Fore.RED + "\nAll port scanned!")
        time.sleep(100000)
        exit()
    except:
        print(Fore.RED + "\nAll port scanned!\n")
        print(Fore.RED + "You got blocked from mcsrvstats apis! Some ports weren't displayed as a minecraft servers.")
        time.sleep(100000)
        exit()

if __name__ == '__main__':
    check()

