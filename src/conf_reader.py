#!/usr/bin/env python3

import json

class ConfReader():
    def __init__(self, filename):
        self.conf = {}
        with open(filename, 'r') as conf_file:
            content = conf_file.read()
            self.conf = json.loads(content)

    def get(self, key):
        return self.conf[key] if key in self.conf else None

    def __getitem__(self, key):
        return self.get(key)
