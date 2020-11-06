#!/usr/bin/python3.8

from sys import platform
from pathlib import Path
import logging

class Constants():
    '''Constant variables like path for the project'''
    def __init__(self):
        if "win" in platform.lower():
            self.path_root = Path("/users/pedro/project_b")
        else:
            # self.path_root = Path("/media/Data/MyDoc/Python/win_registry/")
            self.path_root = Path("/home/peter/Desktop/rm_monthly/testgit/")

    @staticmethod
    def files_list():
        return ("local.json", "meta.json", "mi_proxy.xml", "source.zip", "master.zip",
         "win_registry-master", "logs.log")

    @staticmethod
    def scripts_list():
        return ("constants.py", "launcher.vbs", "updater.py", "win_registry.py")

    def files(self):
        '''return dictionary including the path of all files in "files path"'''
        return {i:self.path_root.joinpath("files",i) for i in self.files_list()}

    def scripts(self):
        '''return dictionary including the path of all files in "scripts path"'''
        return {i:self.path_root.joinpath("scripts",i) for i in self.scripts_list()}

    def url(self):
        '''return dictionary including the URLs"'''
        return {"git_source": r"https://github.com/ccie57960/win_registry/archive/source.zip",
        "git_master": r"https://github.com/ccie57960/win_registry/archive/master.zip",
        "drive_base": (r"https://drive.google.com/uc?id=", r"&export=download")
        }

    def default_settings(self):
        return {"config":{"enable": 1, "server": "127.3.2.1:50000",
        "override": "wifilogin.xfinity.com;konfyanslotto.com;lakonfyanslotto.com;nationlk.com;sports-allstar.net;*github.com;*amazonaws.com;<local>"}}

    def logger(self):
        log_file = self.files()['logs.log']
        if not log_file.is_file():
            with open(log_file, "w+") as pf:
                #create empty logs.log
                pass
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(module)s;%(lineno)d;%(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
