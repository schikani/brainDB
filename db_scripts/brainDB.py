# ==========================================
# Project:   brainDB
# Author:    Shivang Chikani
# Date:      02 Mar 2021
# ==========================================

# This script needs to have micropython available system-wide.
# If it is not available, run install.sh from the root (brainDB)
# It will clone micropython and compile the binaries.
# Module subprocess comes to our rescue and enables us to talk to micropython
# from python3.


import subprocess


class brainDB:

    def __init__(self, name):
        self.name = name
        self._verbose = 0
        self._notClosed = True

    # This function will invoke ubrainDB from micropyton for reading / writing into the database.
    def _initialize(self, command=None):
        talk = subprocess.Popen(
            ["micropython", "-c",
             f"from db_scripts.ubrainDB import ubrainDB as DB; \
            db = DB('{self.name}'); db.verbose({self._verbose}); \
            print(db.{command})"],

            stdout=subprocess.PIPE)

        output = talk.communicate()[0]

        try:
            output = eval(output.strip(b"\n").decode())
        except NameError:
            output = output.strip(b"\n").decode()
        except SyntaxError:
            output = output.strip(b"\n").decode()

        return output

    # This function helps in displaying the message when database is closed.
    def _close_message(self):
        return "Database => '{}' is closed. Use reopen() to open the database again".format(self.name)

    # This function helps in re-opening the database after it is closed.
    def reopen(self):
        self._notClosed = True

    # Verbose can be set to 1 for displaying writing / deleting messages.
    def verbose(self, value):
        if self._notClosed:
            if value >= 1:
                self._verbose = 1

            else:
                self._verbose = 0
        else:
            return self._close_message()

    # This function takes the key and value to be written in the current database.
    def write(self, key, value):

        if self._notClosed:

            if isinstance(key, str):
                key = f"'{key}'"

            if isinstance(value, str):
                value = f"'{value}'"

            message = self._initialize(f"write({key}, {value})")
            return message

        else:
            return self._close_message()

    # This function returns the data given it's key or value from the current database.
    # If a key is given as parameter, it returns value and if value is given as parameter,
    # a list of keys is returned
    def read(self, key=None, value=None):

        if self._notClosed:

            message = ""

            if isinstance(key, str):
                key = f"'{key}'"

            if isinstance(value, str):
                value = f"'{value}'"

            if key is not None:
                message = self._initialize(f"read({key})")
            elif value is not None:
                message = self._initialize(f"read(value = {value})")

            return message

        else:
            return self._close_message()

    # Remove key-value pair/s given the key or value as the parameter.
    def remove(self, key=None, value=None):

        if self._notClosed:

            message = ""

            if isinstance(key, str):
                key = f"'{key}'"

            if isinstance(value, str):
                value = f"'{value}'"

            if key is not None:
                message = self._initialize(f"remove({key})")
            elif value is not None:
                message = self._initialize(f"remove(value = {value})")

            return message

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted keys in a list.
    # If key is given as start_key parameter, the keys after the key (including the given key)
    # to the end of database is returned as a sorted list.
    # If reverse is set True, the list is returned in reverse order.
    def keys(self, start_key=None, reverse=False):

        if self._notClosed:

            message = ""
            if isinstance(start_key, str):
                start_key = f"'{start_key}'"

            if start_key is None and reverse is False:
                message = self._initialize("keys()")
            elif start_key is None and reverse:
                message = self._initialize("keys(reverse = True)")
            elif start_key is not None and reverse is False:
                message = self._initialize(f"keys({start_key})")
            elif start_key is not None and reverse:
                message = self._initialize(f"keys({start_key}, reverse = True)")

            return message

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted values in a list.
    # If key is given as start_key parameter, the values after the value (including the value of given key)
    # to the end of database is returned as a sorted list.
    # if reverse is set True, the list is returned in reverse order.
    def values(self, start_key=None, reverse=False):

        if self._notClosed:

            message = ""
            if isinstance(start_key, str):
                start_key = f"'{start_key}'"

            if start_key is None and reverse is False:
                message = self._initialize("values()")
            elif start_key is None and reverse:
                message = self._initialize("values(reverse = True)")
            elif start_key is not None and reverse is False:
                message = self._initialize(f"values({start_key})")
            elif start_key is not None and reverse:
                message = self._initialize(f"values({start_key}, reverse = True)")

            return message

        else:
            return self._close_message()

    # Get all encoded key - value pairs in a dictionary.
    # Optionally start_key param accepts a key.
    # The keys and values are stored as bytes objects.
    def items(self, start_key=None):

        if self._notClosed:

            if isinstance(start_key, str):
                start_key = f"'{start_key}'"

            if start_key is None:
                message = self._initialize("items()")

            else:
                message = self._initialize(f"items({start_key})")

            return message

        else:
            return self._close_message()

    # Get a list of all the databases including the currently open.
    def databases(self):
        message = self._initialize("databases()")
        return message

    # Remove a database by it's name
    # If it is the current database, it will get erased.
    # In order to completely remove the current Database,
    # this function should be called by the instance of
    # another Database.
    def remove_database(self, name):
        message = self._initialize(f"remove_database('{name}')")
        return message

    # This function helps in closing the current stream.
    # After calling this function, reading / writing  will not work.
    # In order to read / write again to the current instance, call reopen().
    def close(self):
        self._notClosed = False
        if self._verbose == 1:
            return self._close_message()
