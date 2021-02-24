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

# Try to make the database folder if it doesn't exist.
try:
    uos.mkdir("{}".format(DB_FOLDER))

except OSError as exc:
    if exc.args[0] == uerrno.EEXIST:
        pass


class brainDB:
    # Init function collects garbage with gc.collect(), sets the database name,
    # sets verbose and calls self._initialize() function.
    def __init__(self, name, verbose=None):
        gc.collect()
        self._name = name
        self._initialize()
        self._verbose = verbose

    def verbose(self, value):
        if value > 0:
            self._verbose = 1

    # This function will try to open the database.
    def _initialize(self):
        try:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "r+b")
        except OSError:
            self._stream = open("{}/{}".format(DB_FOLDER, self._name), "w+b")

        self._db = btree.open(self._stream)

    # This function returns the data given it's key from the current database.
    def read(self, key):
        try:
            dataB = self._db[b"{}".format(key)]
            try:
                data_to_return = eval(dataB)
            except NameError:
                # Check if the data is type str
                # decode() will decode from bytes to str
                data_to_return = dataB.decode()

            gc.collect()
            return data_to_return

        except KeyError:
            return 'Invalid key!'

        except OSError:
            return "OSError: Can't read from file '{}'".format(self._name)

    # This function takes the key and data to be written to the current database.
    def write(self, key, value):
        try:
            if self._db is not None:
                if b"{}".format(key) in self._db.keys():
                    n = self._if_same_keys(key=b"{}".format(key))
                    self._db[b"({},{})".format(key, n)] = b"{}".format(value)
                    self._db.flush()

                else:
                    self._db[b"{}".format(key)] = b"{}".format(value)
                    self._db.flush()

                if self._verbose == 1:
                    return "Value stored in database: '{}' with type: {}, key: '{}'" \
                        .format(self._name, type(value), key)

                gc.collect()

        except OSError:
            self._db.flush()
            return "Something went wrong while writing to '{}'".format(self._name)

    def _if_same_keys(self, key):

        try:
            _stream = open("{}/.same_keys-{}".format(DB_FOLDER, self._name), "r+b")

        except OSError:
            _stream = open("{}/.same_keys-{}".format(DB_FOLDER, self._name), "w+b")

        _db = btree.open(_stream)

        try:
            value = _db[key]
            n = eval(_db[key]) + 1
            _db[key] = b"{}".format(n)
            _db.flush()

        except KeyError:
            n = 0
            _db[key] = b"0"
            _db.flush()

        _db.close()
        _stream.close()

        return n

    # Iterate over sorted keys in the database getting sorted keys in a list
    def keys_sorted(self):

        sorted_list = []

        for k in self._db:
            try:
                sorted_list.append(eval(k))
            except NameError:
                sorted_list.append(k.decode())

        gc.collect()
        return sorted_list

    # Iterate over sorted keys in the database, starting
    # from the given key as parameter until the end of the database,
    # returning only values.
    # Mind that arguments passed to values_sorted() method are *key* values.
    def values_sorted(self, key):

        sorted_values = []

        for v in self._db.values(b"{}".format(key)):
            try:
                sorted_values.append(eval(v))

            except NameError:
                sorted_values.append(v.decode())

        gc.collect()
        return sorted_values

    # Remove a key-value pair/s given the key or value as the parameter
    def remove(self, key=None, value=None):

        if key is not None:
            try:
                del self._db[b"{}".format(key)]
                self._db.flush()

                if self._verbose == 1:
                    print("Removing Key: '{}'".format(key))

            except KeyError:
                return 'Invalid key!'

            gc.collect()

        elif value is not None:

            keys_found = 0

            for key_, value_ in self._db.items():
                if value_ == b"{}".format(value):
                    keys_found = 1
                    del self._db[key_]
                    self._db.flush()
                    gc.collect()

                    if self._verbose == 1:
                        try:
                            print("Removing Key: '{}' by the given Value: '{}'".format(eval(key_), value))

                        except NameError:
                            print("Removing Key: '{}' by the given Value: '{}'".format(key_.decode(), value))

            if keys_found == 0:
                return "No keys found with Value: '{}'".format(value)

        else:
            return "Enter a key or value to remove key-value pair/s."

    # To be implemented
    def count(self, key=None, value=None):
        pass

    # This function helps in closing the current stream.
    # After calling this function, calling read() / write() functions will cause an OSError
    # Only call this function after all the reading and writing is finished for the current database.
    def close(self):
        self._db.close()
        self._stream.close()
