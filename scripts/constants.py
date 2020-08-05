#!/usr/bin/python3.8

from sys import platform

class Constants():
    '''Constant variables like path for the project'''
    def __init__(self):
        if "win" in platform:
            self.path_root = r"C:\Users\Pedro\project_b\\"
        else:
            self.path_root = r"/home/peter/Desktop/rm_monthly/testgit/"

    def files(self):
        '''return dictionary including the path of all files in "files path"'''
        files = {}
        f = ("local.json", "meta.json", "mi_proxy.xml", "source.zip")

        for i in f:
            files.update({i:f"{self.path_root}{i}"})
        return files

    def scripts(self):
        '''return dictionary including the path of all files in "scripts path"'''
        files = {}
        f = ("constants.py", "launcher.vbs", "updater.py", "win_registry.py")

        for i in f:
            files.update({i:f"{self.path_root}{i}"})
        return files

    def url(self):
        '''return dictionary including the URLs"'''
        return {"git_source": r"https://github.com/ccie57960/win_registry/archive/source.zip",
        "drive_base": (r"https://drive.google.com/uc?id=", r"&export=download")

        }
