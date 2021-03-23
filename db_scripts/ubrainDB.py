# ==========================================
# Project:   ubrainDB
# Author:    Shivang Chikani
# Date:      23 Feb 2021
# ==========================================

import uos
import uerrno
import btree
import gc

__version__ = 1.0.5

# Set a name for the database folder.
DB_FOLDER = "./DB"

# Try to make the database folder if it doesn't exist.
try:
    uos.mkdir("{}".format(DB_FOLDER))

except OSError as exc:
    if exc.args[0] == uerrno.EEXIST:
        pass


class ubrainDB:
    gc.enable()

    def __init__(self, name):
    	self.__version__ = __version__
        self.name = name
        # Define the extension for database
        if not name.endswith(".brain"):
            self._name = self.name + ".brain"
        self._verbose = 0
        self._notClosed = True
        self._db = None
        self._initialize()

    # This function will try to open the database and save it's name.
    def _initialize(self):
        try:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "r+b")
        except OSError:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "w+b")

        self._db = btree.open(self._stream)

    # This function helps in displaying the message when database is closed.
    def _close_message(self):
        return "Database => '{}' is closed. Use reopen() to open the database again".format(self._name)

    # This function helps in re-opening the database after it is closed.
    def reopen(self):
        self._notClosed = True
        return self._initialize()

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

            try:
                display = ""
                if self._db is not None:
                    if self._verbose == 1:
                        display = "Writing to => '{0}' | Key => {1} |" \
                                  " Value => {2}" \
                            .format(self._name, type(key), type(value))

                    self._db[str(key).encode()] = str(value).encode()
                    self._db.flush()

                    return display

            except OSError:
                self._db.flush()
                return "Something went wrong while writing to => '{}' ".format(self._name)
        else:
            return self._close_message()

    # This function returns the data given it's key or value from the current database.
    # If a key is given as parameter, it returns value and if value is given as parameter,
    # a list of keys is returned
    def read(self, key=None, value=None):
        if self._notClosed:
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
                        return "No keys found with Value => {} ".format(type(value))

                    else:
                        return keys

            except OSError:
                return "Can't read from Database => '{}' ".format(self._name)

        else:
            return self._close_message()

    # Remove key-value pair/s given the key or value as the parameter.
    def remove(self, key=None, value=None):
        if self._notClosed:
            if len(self.items()) == 0:
                return "Nothing to remove!"
            display = ""
            if key is not None:
                try:
                    if self._verbose == 1:
                        display = "Removing Key => {} ".format(type(key))
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
                            display = "Removing Key => {} | By Value => {} ".format(type(k), type(value))

                        del self._db[key_]
                        self._db.flush()

                if key_found == 0:
                    return "No keys found with Value => {} ".format(type(value))
                else:
                    return display

            else:
                return "Enter a key or value to remove key-value pair/s"

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted keys in a list.
    # If key is given as start_key parameter, the keys after the key (including the given key)
    # to the end of database is returned as a sorted list.
    # If reverse is set True, the list is returned in reverse order.
    def keys(self, start_key=None, reverse=False):

        if self._notClosed:

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

            if reverse:
                keys.reverse()

            return keys

        else:
            return self._close_message()

    # Iterate over sorted keys in the database getting sorted values in a list.
    # If key is given as start_key parameter, the values after the value (including the value of given key)
    # to the end of database is returned as a sorted list.
    # if reverse is set True, the list is returned in reverse order.
    def values(self, start_key=None, reverse=False):

        if self._notClosed:

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

            if reverse:
                values.reverse()

            return values

        else:
            return self._close_message()

    # Get all encoded key - value pairs in a dictionary.
    # Optionally start_key param accepts a key.
    # The keys and values are stored as bytes objects.
    def items(self, start_key=None):

        if self._notClosed:

            items = {}

            if start_key is not None:
                for k, v in self._db.items(str(start_key).encode()):
                    items[k] = v
            else:
                for k, v in self._db.items():
                    items[k] = v

            return items

        else:
            return self._close_message()

    # Get a list of all the databases including the currently open.
    def databases(self):

        databases = [
            i[0][:i[0].rindex(".brain")]
            for i in uos.ilistdir(DB_FOLDER)
            if i[0].endswith(".brain")
        ]

        return databases

    # Remove a database by it's name.
    # If it is the current database, it will get erased.
    # In order to completely remove the current Database,
    # this function should be called by the instance of
    # another Database.
    def remove_database(self, name):
        name_ = name

        if not name_.endswith(".brain"):
            name_ = name + ".brain"

        try:
            display = ""

            if name_ == self._name:
                display = "Erasing current database => '{}' ".format(name_)
                with open("{}/{}".format(DB_FOLDER, name_), "w") as erase:
                    erase.write("")
                    erase.close()
                self._initialize()

            elif name_ != self._name:
                display = "Removing Database => '{}' ".format(name_)
                uos.remove("{}/{}".format(DB_FOLDER, name_))

            if self._verbose == 1:
                return display

        except OSError:
            return "Database => '{}' not found".format(name_)

    # This function helps in closing the current stream.
    # After calling this function, reading / writing  will not work.
    # In order to read / write again to the current instance, call reopen().
    def close(self):
        self._notClosed = False
        self._db.close()
        self._stream.close()
        if self._verbose == 1:
            return self._close_message()
