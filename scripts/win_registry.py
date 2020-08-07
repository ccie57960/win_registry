#!/usr/bin/python3.8
from os import popen
from re import search
from json import dump, load
import logging
from time import strftime, sleep, time
from getpass import getuser
from updater import Updater
from constants import Constants

logger = Constants().logger()

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
    global logger
    path_local = Constants().files().get("local.json")

    if not path_local.is_file():
        logger.error(f"Not local.json at {path_local}...Trying upgrade")
        if not Updater(logger, force=True).run():
            default_values = {"config":{
            "enable": 1,
            "server": "127.3.2.1:50000",
            "override": "wifilogin.xfinity.com;konfyanslotto.com;lakonfyanslotto.com;nationlk.com;sports-allstar.net;*github.com;*amazonaws.com;<local>"}}
            logger.warning(f"local.json set to defaults: {default_values}")

            with open(path_local, "w+") as pf:
                dump(default_values, pf, indent=1)

            return default_values["config"]

    with open(path_local, "r") as pf:
        values = load(pf)
    return values["config"]

def set_reg():
    default = read_local()
    old = query_intset()
    if default == old:
        return False

    logger.warning(f"Changing config {old=} {default=}")
    cmd = f'''REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d {default["enable"]} /f
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {default["server"]} /f
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "{default["override"]}" /f
'''
    cmd = cmd.split("\n")
    for i in cmd:
        popen(i).read()
    return True

def log_control(size = 100000):
    '''limit the number of lines of logfile to size//2 once size is reached'''
    path_log = Constants().files().get("logs.log")

    with open(path_log) as pf:
        data = pf.readlines()
    if len(data) > size:
        size //= -2
        with open(path_log, "w+") as pf:
            pf.writelines(data[size:])

if __name__ == "__main__":
    logger.info("Start time")
    log_control()
    Updater(logger).run()
    interval = 60 #run every X seconds
    c = 10
    dampening = 60 #60 minutes
    t = time()
    while True:
        if set_reg():
            interval = 5
            dampening = 60
            logger.warning(f"Decreasing validation time to {interval=} (seconds)")
        else:
            if interval == 5:
                dampening -= (interval/60)
                if dampening < 0:
                    logger.warning(f"Validation restored to {interval=} (seconds)")
                    interval = 60
        sleep(interval)
        c -= (interval/60)
        if c < 0:
            logger.info(f"Running for: {(time() - t)//60} mins")
            c = 10
