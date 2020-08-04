#!/usr/bin/python3.8

import urllib.request
import json

class Updater():
    def __init__(self):
        self.urlbase = (r"https://drive.google.com/uc?id=", r"&export=download")
        self.meta_id = r"1gT-wyS4HX8LXpYouMnc5kjvG-enRReDm"
        # https://drive.google.com/file/d//view?usp=sharing
        # self.meta_id = "1VmRLM85F4xRX0BDhpxvt5y9JF9FIXB1L"

    def get_meta(self):
        url = r"https://drive.google.com/uc?id=1gT-wyS4HX8LXpYouMnc5kjvG-enRReDm&export=download"
        o = urllib.request.urlopen(url)
        data = o.read()
        data = data.decode("utf-8")
        o.close()
        return json.loads(data)
