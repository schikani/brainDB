# ==========================================
# Author: Shivang Chikani
# Project: db_scripts
# Date:   2 Mar 2021
# ==========================================


import subprocess
import json

with open('./db_scripts/commands.json') as c:
    c = json.load(c)

COMMANDS = c["COMMANDS"]


class brainDB:
    def __init__(self, name):
        self.name = name
        self._verbose = 0
        self._close = 0

    def _initialize(self, command, arg1=None, arg2=None):
        output = ""

        if arg1 is None and arg2 is None:
            test = subprocess.Popen(
                ["./db_scripts/micropython", "./db_scripts/ubrainDB_helper.py", f"{self._close}", f"{self._verbose}", f"{self.name}",
                 f"{command}"],
                stdout=subprocess.PIPE)
            output = test.communicate()[0]
            try:
                output = eval(output.strip().decode())
            except NameError:
                output = output.strip().decode()
            except SyntaxError:
                output = output.strip().decode()

        elif arg1 is not None and arg2 is None:
            test = subprocess.Popen(
                ["./db_scripts/micropython", "./db_scripts/ubrainDB_helper.py", f"{self._close}", f"{self._verbose}", f"{self.name}",
                 f"{command}", f"{arg1}"],
                stdout=subprocess.PIPE)
            output = test.communicate()[0]
            try:
                output = eval(output.strip().decode())
            except NameError:
                output = output.strip().decode()
            except SyntaxError:
                output = output.strip().decode()

        elif arg1 is not None and arg2 is not None:
            test = subprocess.Popen(
                ["./db_scripts/micropython", "./db_scripts/ubrainDB_helper.py", f"{self._close}", f"{self._verbose}", f"{self.name}",
                 f"{command}", f"{arg1}",
                 f"{arg2}"],
                stdout=subprocess.PIPE)
            output = test.communicate()[0]
            try:
                output = eval(output.strip().decode())
            except NameError:
                output = output.strip().decode()
            except SyntaxError:
                output = output.strip().decode()
        return output

    def verbose(self, value):
        if value >= 1:
            self._verbose = 1

        else:
            self._verbose = 0

    # Don't write values in plain string, wrap it in list, set etc.
    def write(self, key, value):
        message = self._initialize(COMMANDS[0], key, value)
        return message

    def read(self, key=None, value=None):

        message = ""

        if key is not None:
            message = self._initialize(COMMANDS[1], key)
        elif value is not None:
            message = self._initialize(COMMANDS[2], value)

        return message

    def remove(self, key=None, value=None):

        message = ""

        if key is not None:
            message = self._initialize(COMMANDS[3], key)
        elif value is not None:
            message = self._initialize(COMMANDS[4], value)

        return message

    def keys(self, start_key=None, reverse=False):

        message = ""

        if start_key is None and reverse is False:
            message = self._initialize(COMMANDS[5])
        elif start_key is None and reverse:
            message = self._initialize(COMMANDS[6])
        elif start_key is not None and reverse is False:
            message = self._initialize(COMMANDS[7], start_key)
        elif start_key is not None and reverse:
            message = self._initialize(COMMANDS[8], start_key)

        return message

    def values(self, start_key=None, reverse=False):

        message = ""

        if start_key is None and reverse is False:
            message = self._initialize(COMMANDS[9])
        elif start_key is None and reverse:
            message = self._initialize(COMMANDS[10])
        elif start_key is not None and reverse is False:
            message = self._initialize(COMMANDS[11], start_key)
        elif start_key is not None and reverse:
            message = self._initialize(COMMANDS[12], start_key)

        return message

    def items(self, start_key=None):
        if start_key is None:
            message = self._initialize(COMMANDS[13])

        else:
            message = self._initialize(COMMANDS[14], start_key)

        return message

    def databases(self):
        message = self._initialize(COMMANDS[15])
        return message

    def close(self):
        self._close = 1
        message = self._initialize(COMMANDS[16])
        return message
