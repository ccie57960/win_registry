#!/usr/bin/python3.8
from os import popen, path
from re import search
from json import dump, load
import logging
from time import strftime, sleep, time
from getpass import getuser

interval = 60 #run every X seconds
path_root = r"C:\Users\Pedro\project_b"
path_log = fr"{path_root}\files\logs.log"
path_local = fr"{path_root}\files\local.json"

def query_intset():
    cli = 'REG QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings"'
    proxy = {"enable": 0, "server":None, "override":None}
    o = popen(cli).read()
    proxy["enable"] = int(search("ProxyEnable\s+REG_DWORD\s+0x(\d)", o)[1])
    if a := search("ProxyServer\s+REG_SZ\s+([\d\.:]+)", o):
        proxy["server"] = a[1]
    if a := search("ProxyOverride\s+REG_SZ\s+(.+)", o):
        proxy["override"] = a[1]
    return proxy

def read_local():
    global path_local

    if not path.exists(path_local):
        logit(f"Not local.json at {path_local}")
        default_values = {"enable": 1,
    "server": "127.3.2.1:50000",
    "override": "wifilogin.xfinity.com;konfyanslotto.com;lakonfyanslotto.com;nationlk.com;sports-allstar.net;*amazonaws.com;<local>"}

        with open(path_local, "w+") as pf:
            dump(default_values, pf, indent=1)

        return default_values

    with open(path_local, "r") as pf:
        values = load(pf)
    return values["config"]

def set_reg():
    default = read_local()
    old = query_intset()
    if default == old:
        return

    logit(f'Changing config\n\t{old=}\n\t{default=}')
    cmd = f'''REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d {default["enable"]} /f
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {default["server"]} /f
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "{default["override"]}" /f
'''
    cmd = cmd.split("\n")
    for i in cmd:
        popen(i).read()


def logit(s):
    global path_log
    with open(path_log, "a+") as pf:
        pf.write(f'{strftime("%x %X")} - user: {getuser()} - {s}\n')

def log_control():
    '''limit the number of lines of logfile to size//2 once size is reached'''
    global path_log
    size = 100000
    with open(path_log) as pf:
        data = pf.readlines()
    if len(data) > size:
        size //= -2
        with open(path_log, "w+") as pf:
            pf.writelines(data[size:])

if __name__ == "__main__":
    logit(f'Start time')
    log_control()
    c = 0
    t = time()
    while True:
        set_reg()
        sleep(interval)
        c += 1
        if not (c % 5):
           logit(f'Running for: {(time() - t)//60} mins')
           c = 0
