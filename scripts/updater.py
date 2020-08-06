#!/usr/bin/python3.8

import urllib.request
import json
from zipfile import ZipFile
from constants import Constants
from os import remove

class Updater():
    def __init__(self):
        c = Constants()
        self.files = c.files()
        self.url = c.url()
        self.os_delimiter = c.os_delimiter
        self.path_root = c.path_root

    def get_meta(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        self.source = {}
        try:
            with urllib.request.urlopen(self.url["git_source"]) as data:
                o = data.read()
            with open(self.files["source.zip"], "wb+") as pf:
                pf.write(o)
                pf.seek(0)
                with ZipFile(pf) as z:
                    if 'win_registry-source/meta.json' in z.namelist():
                        self.source = json.loads(z.read('win_registry-source/meta.json'))
            remove(f'{self.files["source.zip"]}')
        except Exception as e:
            # print(e)#pending: logging a least
            pass

    def new_version(self):
        '''return True if new version available by comparing
        meta.json (source brach) vs local.json (files directory)
        c'''
        if self.source.get("version") == None:
            return False

        with open(self.file["local.json"]) as pf:
            local = json.load(pf)

        return self.source.get("version") > local.get("meta", {}).get("version", 0)

    def upgrade(self):
        pass



if __name__ == "__main__":
    obj = Updater()
    # obj.get_meta()
    obj.get_meta()
    # print(obj.source)
    print(obj.new_version())
