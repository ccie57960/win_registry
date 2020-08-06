#!/usr/bin/python3.8

import urllib.request
import json
from zipfile import ZipFile
from constants import Constants
from os import remove
from shutil import copytree, rmtree

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
        version = self.source.get("meta", {}).get("version")
        if version == None:
            return False

        with open(self.files["local.json"]) as pf:
            local = json.load(pf)
        return version > local.get("meta", {}).get("version", 0)

    def upgrade(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        try:
            with urllib.request.urlopen(self.url["git_master"]) as data:
                o = data.read()
            with open(self.files["master.zip"], "wb+") as pf:
                pf.write(o)
                pf.seek(0)
                with ZipFile(pf) as z:
                    z.extractall(f"{self.path_root}files")

            copytree(f"{self.files['win_registry-master']}{self.os_delimiter}files",
             f"{self.path_root}files", dirs_exist_ok=True)
            copytree(f"{self.files['win_registry-master']}{self.os_delimiter}scripts",
             f"{self.path_root}scripts", dirs_exist_ok=True)
            rmtree(self.files['win_registry-master'])
            remove(self.files["master.zip"])
        except Exception as e:
            # print(e)#pending: logging a least
            pass

    def run(self):
        self.get_meta()
        if self.new_version():
            self.upgrade()
        else:
            #log here
            pass


if __name__ == "__main__":
    Updater().run()
