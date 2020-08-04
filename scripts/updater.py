#!/usr/bin/python3.8

import urllib.request
import json
from zipfile import ZipFile

class Updater():
    def __init__(self):
        self._urlbase = (r"https://drive.google.com/uc?id=", r"&export=download")
        self._url = r"https://github.com/ccie57960/win_registry/archive/source.zip"
        self._path = r"/home/peter/Desktop/rm_monthly/testgit/source.zip"

    def get_meta(self):
        dict = {}
        try:
            with urllib.request.urlopen(self._url) as data:
                o = data.read()
                with open(self._path, "wb+") as pf:
                    pf.write(o)

            with ZipFile(self._path) as z:
                if 'win_registry-source/meta.json' in z.namelist():
                    dict = json.loads(z.read('win_registry-source/meta.json'))
        except:
            #pending: logging a least
            pass
        return dict

if __name__ == "__main__":
    obj = Updater()
    d = obj.get_meta()
    print(d)
