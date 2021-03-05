# ==========================================
# Author:    Shivang Chikani
# Project:   ubrainDB
# Date:      23 Feb 2021
# ==========================================

import uos
import uerrno
import btree
import gc

# Set a name for the database folder.
DB_FOLDER = "./DB"

# Try to make the database folder if it doesn't exist.
try:
    uos.mkdir("{}".format(DB_FOLDER))

except OSError as exc:
    if exc.args[0] == uerrno.EEXIST:
        pass


class ubrainDB:

    def __init__(self, name):
        self.name = name
        gc.collect()
        # Define the extension for database
        if not name.endswith(".brain"):
            self.name = name + ".brain"

        self._verbose = 0
        self._notClosed = True
        self._db = None

        self._initialize()

    # This function will try to open the database and save it's name
    def _initialize(self):
        if self._notClosed:
            try:
                self._stream = open("{}/{}".format(DB_FOLDER, self.name), "r+b")
            except OSError:
                self._stream = open("{}/{}".format(DB_FOLDER, self.name), "w+b")

            self._db = btree.open(self._stream)

        else:
            return "Database => '{}' is closed.".format(self.name)

    # verbose can be set to 1 for displaying writing / deleting messages.
    def verbose(self, value):
        if value >= 1:
            self._verbose = 1

        else:
            self._verbose = 0

    # This function takes the key and value to be written in the current database.
    def write(self, key, value):

        gc.collect()

        try:
            display = ""
            if self._db is not None:
                if self._verbose == 1:
                    display = "Writing to => {0} | Key => {1} |" \
                              " Value => {2}" \
                        .format(self.name, type(key), type(value))

                self._db[str(key).encode()] = str(value).encode()
                self._db.flush()

                return display

        except OSError:
            self._db.flush()
            return "Something went wrong while writing to: {}".format(self.name)

    # This function returns the data given it's key or value from the current database.
    # If a key is given as parameter, it returns value and if value is given as parameter,
    # a list of keys is returned
    def read(self, key=None, value=None):
        try:
            if key is not None:
                try:
                    value_B = self._db[str(key).encode()]

                    try:
                        value_ = eval(value_B)

                    except NameError:
                        # Check if the data is type str
                        # decode() will decode from bytes to str
                        value_ = value_B.decode()

                    except SyntaxError:
                        # Check for any special characters
                        value_ = value_B.decode()

                    gc.collect()
                    return value_

                except KeyError:
                    return "Invalid key!"

            elif value is not None:

                keys = []

                for key_, value_ in self._db.items():
                    if value_ == str(value).encode():
                        try:
                            keys.append(eval(key_))

                        except NameError:
                            keys.append(key_.decode())

                        except SyntaxError:
                            keys.append(key_.decode())

                if len(keys) == 0:
                    return "No keys found with Value => {}".format(type(value))

                else:
                    return keys

        except OSError:
            return "Can't read from Database => {} ".format(self.name)

    # Remove key-value pair/s given the key or value as the parameter
    def remove(self, key=None, value=None):
        display = ""
        if key is not None:
            try:
                if self._verbose == 1:
                    display = "Removing Key => {}".format(type(key))
                del self._db[str(key).encode()]
                self._db.flush()

                return display

            except KeyError:
                return "Invalid key!"

        elif value is not None:

            key_found = 0

            for key_, value_ in self._db.items():
                if value_ == str(value).encode():
                    key_found = 1

                    if self._verbose == 1:
                        try:
                            k = eval(key_)
                        except NameError:
                            k = key_.decode()
                        except SyntaxError:
                            k = key_.decode()
                        display = "Removing Key => {} | By Value => {}".format(type(k), type(value))

                    del self._db[key_]
                    self._db.flush()

            gc.collect()

            if key_found == 0:
                return "No keys found with Value => {}".format(type(value))
            else:
                return display

        else:
            return "Enter a key or value to remove key-value pair/s"

    # Iterate over sorted keys in the database getting sorted keys in a list
    # If key is given as start_key parameter, the keys after the key (including the given key)
    # to the end of database is returned as a sorted list
    # if reverse is set True, the list is returned in reverse order
    def keys(self, start_key=None, reverse=False):

        keys = []

        if start_key is not None:
            for k in self._db.keys(str(start_key).encode()):
                try:
                    keys.append(eval(k))
                except NameError:
                    keys.append(k.decode())
                except SyntaxError:
                    keys.append(k.decode())
        else:
            for k in self._db.keys():
                try:
                    keys.append(eval(k))
                except NameError:
                    keys.append(k.decode())
                except SyntaxError:
                    keys.append(k.decode())

        gc.collect()
        if reverse:
            keys.reverse()

        return keys

    # Iterate over sorted keys in the database getting sorted values in a list
    # If key is given as start_key parameter, the values after the value (including the value of given key)
    # to the end of database is returned as a sorted list
    # if reverse is set True, the list is returned in reverse order
    def values(self, start_key=None, reverse=False):

        values = []

        if start_key is not None:
            for v in self._db.values(str(start_key).encode()):
                try:
                    values.append(eval(v))
                except NameError:
                    values.append(v.decode())
                except SyntaxError:
                    values.append(v.decode())

        else:
            for v in self._db.values():
                try:
                    values.append(eval(v))
                except NameError:
                    values.append(v.decode())
                except SyntaxError:
                    values.append(v.decode())

        gc.collect()
        if reverse:
            values.reverse()

        return values

    # Get all encoded key - value pairs in a dictionary.
    # Optionally start_key param accepts a key
    # The keys and values are stored as bytes objects
    def items(self, start_key=None):

        items = {}

        if start_key is not None:
            for k, v in self._db.items(str(start_key).encode()):
                items[k] = v
        else:
            for k, v in self._db.items():
                items[k] = v

        return items

    # Get a list of all the databases including the currently open
    def databases(self):

        databases = [
            i[0][:i[0].rindex(".brain")]
            for i in uos.ilistdir(DB_FOLDER)
            if i[0].endswith(".brain")
        ]

        gc.collect()
        return databases

    # Remove a database by it's name
    # If it is the current database, it will get erased.
    # In order to completely remove the current Database,
    # this function should be called by the instance of
    # another Database
    def remove_database(self, name):
        name_ = name

        if not name_.endswith(".brain"):
            name_ = name + ".brain"

        try:
            display = ""

            if name_ == self.name:
                display = "Erasing current database => '{}' ".format(name_)
                with open("{}/{}".format(DB_FOLDER, name_), "w") as erase:
                    erase.close()
                self._initialize()

            elif name_ != self.name:
                display = "Removing Database => '{}' ".format(name_)
                uos.remove("{}/{}".format(DB_FOLDER, name_))

            if self._verbose == 1:
                return display

        except OSError:
            return "Database => '{}' not found".format(name_)

    # This function helps in closing the current stream.
    # After calling this function, calling read() / write() functions will cause an OSError
    # Only call this function after all the reading and writing is finished for the current database.
    def close(self):
        self._notClosed = False
        self._db.close()
        self._stream.close()
        if self._verbose == 1:
            return self._initialize()
