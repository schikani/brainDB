# brainDB

## About:
* This project is based on the btree module from MicroPyton which is based on BerkelyDB library
* Btrees are efficient in retrieving values by given keys.

## Usage:
* Micropython datatypes like: int, str, list, tuple, set, dict, bytes, bytearray, bool can be used both as keys and values for the database.

## Examples:
```python
from brainDB import brainDB as DB

db_name1 = DB("name1")
db_name1.write(0, [i for i in range(100)])
db_name1.read(0)

db_name2 = DB("name2")
db_name2.write({3:2, 1:5}, "myValue")
db_name2.read({3:2, 1:5})
```

## Note:
* While writing very big values, the file can be corrupted and unusable.
* It is better to distribute the values with more keys,
* Or distribute data across different databases. This can prevent file corruption.
