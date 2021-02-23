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
        self._verbose = verbose
        self._initialize()

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
                # Check if the data is type: str, decode() will decode from bytes to str
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
                self._db[b"{}".format(key)] = b"{}".format(value)
                self._db.flush()
                gc.collect()
                if self._verbose == 1:
                    return "Value stored in database: '{}' with type: {}, key: '{}'".format(self._name, type(value), key)
        except OSError:
            self._db.flush()
            return "Something went wrong while writing to '{}'".format(self._name)

    # This function helps in closing the current stream.
    # After calling this function, calling read() / write() functions will cause an OSError
    # Only call this function after all the reading and writing is finished for the current database.
    def close(self):
        self._db.close()
        self._stream.close()
