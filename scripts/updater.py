#!/usr/bin/python3.8

import urllib.request
import json
from zipfile import ZipFile
from constants import Constants
from os import remove
from shutil import copytree, rmtree

class Updater():
    def __init__(self, logger, force=False):
        c = Constants()
        self.files = c.files()
        self.url = c.url()
        self.path_root = c.path_root
        self.force = force
        self.logger = logger
        # self.logger = c.logger()

    def get_meta(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        self.source = {}
        try:
            with urllib.request.urlopen(self.url["git_source"]) as data:
                o = data.read()
        except Exception as e:
            self.logger.error(f'Tring "urlopen({self.url["git_source"]}", Got:{e}')
            return False
        else:
            with open(self.files["source.zip"], "wb+") as pf:
                pf.write(o)
                pf.seek(0)
                with ZipFile(pf) as z:
                    if 'win_registry-source/meta.json' in z.namelist():
                        self.source = json.loads(z.read('win_registry-source/meta.json'))
            remove(f'{self.files["source.zip"]}')
            return True


    def new_version(self):
        '''return True if new version available by comparing
        meta.json (source brach) vs local.json (files directory)
        c'''
        if self.files["meta.json"].is_file():
            with open(self.files["meta.json"]) as pf:
                meta = json.load(pf).get("meta", {}).get("version", 0)
        else:
            meta = 0
            self.logger.error(f'{self.files["meta.json"]} NotFound')
        return self.source["meta"]["version"] > meta

    def upgrade(self):
        '''download source branch from github.
        store meta.json in self.source:dict
        '''
        try:
            with urllib.request.urlopen(self.url["git_master"]) as data:
                o = data.read()
        except Exception as e:
            self.logger.error(f'Tring "urlopen({self.url["git_master"]}", Got:{e}')
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
            self.logger.info(f'Successfully upgraded')


    def run(self):
        if self.force:
            self.logger.info(f'Forcing upgrade...')
            self.upgrade()
            return True

        elif self.get_meta() and self.new_version():
            self.logger.info(f'New version available, upgrading...')
            self.upgrade()
            return True
        else:
            return False


if __name__ == "__main__":
    Updater(Constants().logger()).run()
