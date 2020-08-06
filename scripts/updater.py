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
        self.path_root = c.path_root

    def get_meta(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        self.source = {}
        try:
            with urllib.request.urlopen(self.url["git_source"]) as data:
                o = data.read()
        except Exception as e:
            # print(e)#pending: logging a least
            pass
        else:
            with open(self.files["source.zip"], "wb+") as pf:
                pf.write(o)
                pf.seek(0)
                with ZipFile(pf) as z:
                    if 'win_registry-source/meta.json' in z.namelist():
                        self.source = json.loads(z.read('win_registry-source/meta.json'))
            remove(f'{self.files["source.zip"]}')


    def new_version(self):
        '''return True if new version available by comparing
        meta.json (source brach) vs local.json (files directory)
        c'''
        lastest_version = self.source.get("meta", {}).get("version")
        if lastest_version == None:
            return False

        with open(self.files["meta.json"]) as pf:
            meta = json.load(pf)
        return lastest_version > meta.get("meta", {}).get("version", 0)

    def upgrade(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        try:
            with urllib.request.urlopen(self.url["git_master"]) as data:
                o = data.read()
        except Exception as e:
            # print(e)#pending: logging a least
            pass
        else:
            with open(self.files["master.zip"], "wb+") as pf:
                pf.write(o)
                pf.seek(0)
                with ZipFile(pf) as z:
                    z.extractall(self.path_root.joinpath("files"))

            copytree(self.files['win_registry-master'].joinpath("files"),
                self.path_root.joinpath("files"), dirs_exist_ok=True)
            copytree(self.files['win_registry-master'].joinpath("scripts"),
                self.path_root.joinpath("scripts"), dirs_exist_ok=True)

            rmtree(self.files['win_registry-master'])
            remove(self.files["master.zip"])


    def run(self):
        self.get_meta()
        # print(f"{self.source=}")
        if self.new_version():
            self.upgrade()
            #**log here
            # print("upgrading")
            return True
        else:
            # print("NO upgrading")
            #**log here
            return False


if __name__ == "__main__":
    Updater().run()
