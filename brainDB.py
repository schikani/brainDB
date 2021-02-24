# ==========================================
# Author: Shivang Chikani
# Project: brainDB
# Date:   23 Feb 2021
# ==========================================

import uos
import uerrno
import btree
import gc

# Set a name for the database folder.
DB_FOLDER = "./DB"

# All the names of different databases are stored in this file
DB_NAMES = ".databases"

# Try to make the database folder if it doesn't exist.
try:
    uos.mkdir("{}".format(DB_FOLDER))

except OSError as exc:
    if exc.args[0] == uerrno.EEXIST:
        pass


class brainDB:

    def __init__(self, name):
        gc.collect()
        self._name = name
        self._verbose = 0
        # Create a tuple of db name for adding it later in _initialize()
        self._dbID = (self._name, self._name)
        self._initialize()

    # This function will try to open the database and save it's name
    # in DB_NAMES file
    def _initialize(self):

        try:
            self._db_names_stream = open("{}/{}".format(DB_FOLDER, DB_NAMES), "r+b")
        except OSError:
            self._db_names_stream = open("{}/{}".format(DB_FOLDER, DB_NAMES), "w+b")

        self._db_names = btree.open(self._db_names_stream)
        self._db_names[str(self._name).encode()] = str(self._name).encode()
        self._db_names.flush()


        try:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "r+b")
        except OSError:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "w+b")

        self._db = btree.open(self._stream)

    # Return a list of all the databases
    def databases(self):

        databases = []

        for d in self._db_names:
            databases.append(d.decode())

        gc.collect()
        return databases


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
            if self._db is not None:
                self._db[str(key).encode()] = str(value).encode()
                self._db.flush()

                if self._verbose == 1:
                    return "Writing to> Database: {} | Type: {} | Key: {}" \
                        .format(self._name, type(value), key)

        except OSError:
            self._db.flush()
            return "Something went wrong while writing to> {}".format(self._name)


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
                    return "No keys found with Value> {}".format(value)

                else:
                    return keys

        except OSError:
            return "Can't read from file> {}".format(self._name)


    # Remove key-value pair/s given the key or value as the parameter
    def remove(self, key=None, value=None):
        if key is not None:
            try:
                if self._verbose == 1:
                    print("Removing Key> {}".format(key))
                del self._db[str(key).encode()]
                self._db.flush()

            except KeyError:
                return "Invalid key!"

        elif value is not None:

            key_found = 0

            for key_, value_ in self._db.items():
                if value_ == str(value).encode():
                    key_found = 1
                    del self._db[key_]
                    self._db.flush()

                    if self._verbose == 1:
                        try:
                            print("Removing> Key: {} | Given Value: {}".format(eval(key_), value))

                        except NameError:
                            print("Removing> Key: {} | Given Value: {}".format(key_.decode(), value))

                        except SyntaxError:
                            print("Removing> Key: {} | Given Value: {}".format(key_.decode(), value))

            gc.collect()

            if key_found == 0:
                return "No keys found with Value> {}".format(value)

        else:
            return "Enter a key or value to remove key-value pair/s."


    # Iterate over sorted keys in the database getting sorted keys in a list
    # If key is given as start_key parameter, the keys after the key (including the given key)
    # to the end of database is returned as a sorted list
    # if reverse is set True, the list is returned in reverse order
    def sorted_keys(self, start_key=None, reverse=False):

        sorted_keys = []

        if start_key is not None:
            for k in self._db.keys(str(start_key).encode()):
                try:
                    sorted_keys.append(eval(k))
                except NameError:
                    sorted_keys.append(k.decode())
                except SyntaxError:
                    sorted_keys.append(k.decode())
        else:
            for k in self._db.keys():
                try:
                    sorted_keys.append(eval(k))
                except NameError:
                    sorted_keys.append(k.decode())
                except SyntaxError:
                    sorted_keys.append(k.decode())

        gc.collect()
        if reverse:
            sorted_keys.reverse()

        return sorted_keys


    # Iterate over sorted keys in the database getting sorted values in a list
    # If key is given as start_key parameter, the values after the value (including the value of given key)
    # to the end of database is returned as a sorted list
    # if reverse is set True, the list is returned in reverse order
    def sorted_values(self, start_key=None, reverse=False):

        sorted_values = []

        if start_key is not None:
            for v in self._db.values(str(start_key).encode()):
                try:
                    sorted_values.append(eval(v))
                except NameError:
                    sorted_values.append(v.decode())
                except SyntaxError:
                    sorted_values.append(v.decode())

        else:
            for v in self._db.values():
                try:
                    sorted_values.append(eval(v))
                except NameError:
                    sorted_values.append(v.decode())
                except SyntaxError:
                    sorted_values.append(v.decode())

        gc.collect()
        if reverse:
            sorted_values.reverse()

        return sorted_values


    # Get all encoded key - value pairs in a dictionary.
    # Optionally start_key param accepts a key
    # The keys and values are stored as bytes objects
    def get_items(self, start_key=None):
        items = {}

        if start_key is not None:
            for k, v in self._db.items(str(start_key).encode()):
                items[k] = v

        else:
            for k, v in self._db.items():
                items[k] = v


        return items


    # This function helps in closing the current stream.
    # After calling this function, calling read() / write() functions will cause an OSError
    # Only call this function after all the reading and writing is finished for the current database.
    def close(self):
        self._db.close()
        self._stream.close()
        self._db_names.close()
        self._db_names_stream.close()
