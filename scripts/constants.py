#!/usr/bin/python3.8

from sys import platform

class Constants():
    '''Constant variables like path for the project'''
    def __init__(self):
        self.os_delimiter = "\\"
        if "win" in platform:
            self.path_root = r"C:\Users\Pedro\project_b\\"
        else:
            self.os_delimiter = "/"
            self.path_root = r"/media/Data/MyDoc/Python/win_registry/"
            self.path_root = r"/home/peter/Desktop/rm_monthly/testgit/"

    def files(self):
        '''return dictionary including the path of all files in "files path"'''
        f = ("local.json", "meta.json", "mi_proxy.xml", "source.zip", "master.zip",
         "win_registry-master")
        return {i:f"{self.path_root}files{self.os_delimiter}{i}" for i in f}

    def scripts(self):
        '''return dictionary including the path of all files in "scripts path"'''
        f = ("constants.py", "launcher.vbs", "updater.py", "win_registry.py")
        return {i:f"{self.path_root}scripts{self.os_delimiter}{i}" for i in f}

    def url(self):
        '''return dictionary including the URLs"'''
        return {"git_source": r"https://github.com/ccie57960/win_registry/archive/source.zip",
        "git_master": r"https://github.com/ccie57960/win_registry/archive/master.zip",
        "drive_base": (r"https://drive.google.com/uc?id=", r"&export=download")

        }
