#!/usr/bin/env python3
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from platform import system

# @dataclass
class os_sys(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Darwin"
    UNKNOWN = "Unknown"

@dataclass(slots=True)
class Wifi:
    ssid: str
    password: str

    def __str__(self) -> str:
        return f"SSID: {self.ssid}\tPassword: {self.password}"

#####
### Variables
#####
current_system = system()


#####
### Functions
#####

def print_wifi(list_of_wifi: list) -> None:
    for i in list_of_wifi:
        print(i)
#####
### Windows Os
#####
def windows():
    raise NotImplementedError("Windows is not supported yet")

#####
### Linux Os
#####
def linux_get_list_of_saved_networks():
    list_of_networks = list()
    list_of_networks = subprocess.check_output(["ls", "/etc/NetworkManager/system-connections/"]).decode("utf-8").splitlines()
    return list_of_networks

def linux_get_list_of_wifi(list_of_networks) -> list[Wifi]:
    list_of_wifi = list()
    for i in list_of_networks:
        ssid = re.sub(r'.nmconnection', '', i)
        # password = subprocess.check_output(["sudo", "cat", "/etc/NetworkManager/system-connections/" + ssid]).decode("utf-8")
        password = subprocess.check_output(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid]).decode("utf-8")
        list_of_wifi.append(Wifi(ssid, password))
    return list_of_wifi

def linux():
    list_of_networks = linux_get_list_of_saved_networks()
    list_of_wifi = linux_get_list_of_wifi(list_of_networks)
    print_wifi(list_of_wifi)

#####
### Mac OS
#####
def mac():
    raise NotImplementedError("Mac is not supported yet")


def main() -> None:
    if (current_system == os_sys.WINDOWS.value):
        windows()
    elif (current_system == os_sys.LINUX.value):
        linux()
    elif (current_system == os_sys.MAC.value):
        mac()
    else:
        print("Unknown Operating System")

if __name__=="__main__":
    main()