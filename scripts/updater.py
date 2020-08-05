#!/usr/bin/python3.8

import urllib.request
import json
from zipfile import ZipFile
from constants import Constants

class Updater():
    def __init__(self):
        # self._urlbase = (r"https://drive.google.com/uc?id=", r"&export=download")
        # self._url = r"https://github.com/ccie57960/win_registry/archive/source.zip"
        # self._path = r"/home/peter/Desktop/rm_monthly/testgit/source.zip"
        # self._path_root = r"C:\Users\Pedro\project_b"
        # self._path_root = r"/home/peter/Desktop/rm_monthly/testgit/"
        c = Constants()
        self.files = c.files()
        self.url = c.url()

    def get_meta(self):
        '''download source brach from github.
        store meta.json in self.source:dict
        '''
        self.source = {}
        try:
            # with urllib.request.urlopen(self._url) as data:
            with urllib.request.urlopen(self.url["git_source"]) as data:
                o = data.read()
                # with open(self._path, "wb+") as pf:
                with open(self.files["source.zip"], "wb+") as pf:
                    pf.write(o)

            with ZipFile(self.files["source.zip"]) as z:
                if 'win_registry-source/meta.json' in z.namelist():
                    self.source = json.loads(z.read('win_registry-source/meta.json'))
        except Exception as e:
            # print(e)#pending: logging a least
            pass


    def new_version(self):
        '''return True if new version available'''
        if self.source.get("version") == None:
            return False

        # path_local = fr"{path_root}/files/local.json"
        with open(self.file["local.json"]) as pf:
            local = json.load(pf)

        return self.source.get("version") > local.get("meta", {}).get("version", 0)

if __name__ == "__main__":
    obj = Updater()
    obj.get_meta()
    print(obj.source)
    print(obj.new_version())
