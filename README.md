# brainDB
![alt text](https://github.com/schikani/brainDB/blob/main/brainDB.png)

## About:
* This project is based on the btree module from [MicroPython](https://github.com/micropython/micropython) which is based on [BerkelyDB](https://www.oracle.com/database/technologies/related/berkeleydb.html) library.
* Btrees are efficient in retrieving values from given keys.

## Usage:
* Micropython datatypes like: **int, str, list, tuple, set, dict, bytes, bytearray, bool** can be used both as keys and values for the database.
* brainDB is compatible with any device running MicroPython with btree module in it like: **ESP8266, ESP32, Unix etc.**

## Examples:
```python
from brainDB import brainDB as DB

some_list = [i for i in range(100)]
# if verbose is set to 1, it displays information while writing
db_name1 = DB("name1", verbose=1) 
db_name1.write(key=0, value=some_list)
db_name1.read(key=0)

db_name1.write("abc", (5, 10, 15, 20, 25))
db_name1.read("abc")

db_name2 = DB("name2")
db_name2.write({3, 4, 5, 6}, "myValue")
db_name2.read({3, 4, 5, 6})

some_dict = {
    "something":"something more",
    7:[0, 1, 2]
}
db_name3 = DB("name3")
db_name3.write(key=some_dict, value="oopsydoopsy")
db_name3.read(some_dict)

db_name1.close()
db_name2.close()
db_name3.close()
```

## Note:
* While writing very big values, the file can be corrupted and unusable.
* It is better to distribute the values with more keys,
* Or distribute data across different databases. This can prevent file corruption.
