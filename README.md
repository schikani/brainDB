# brainDB (beta)
![alt text](https://github.com/schikani/brainDB/blob/main/brainDB.png)

## About:
* This project is based on the btree module from [MicroPython](https://github.com/micropython/micropython) which is based on [BerkelyDB](https://www.oracle.com/database/technologies/related/berkeleydb.html) library.
* Btrees are efficient in retrieving values from given keys. Both keys and values are stored in bytes objects.
* Python datatypes like: **int, float, str, list, tuple, set, dict, bytes, bytearray, bool** can be used both as keys and values for the database.
* brainDB is compatible for both **python3** and **micropython**
* Because brainDB package is compatible with python3, it is possible to create the database for later use in micropython versions of micro-controllers.
## Possible use cases:
* Data Logging from sensors.
* Storing Wifi credentials in ESP8266 / ESP32 boards.

* Can be used to store datasets efficiently for training Machine Learning models as well as storing weights, biases etc for using it in future predictions.
* * *
## class brainDB / ubrainDB:
|Use|Function
|-|-|

|Create a new database by giving it a name<br>The database file is created inside "DB" folder if it doesn't exist. The path can be changed in "ubrainDB.py"|`db = DB("someName")`<br>`db2 = DB("anotherName")`|

|Create a new database by giving it a name<br>The database file is created inside "DB" folder if it doesn't exist. The path can be changed in "brainDB.py"|`db = DB("someName")`<br>`db2 = DB("anotherName")`|

|Get the names of all the databases in a list|`db.databases()`|
|Set verbose (default is set to 0)<br>If set to 1, it displays information while writing / removing in the database|`db.verbose(1)`|
|Write key - value pairs to the current database. The first argument is key and second is value|`db.write({777}, 0.12)`<br>`db.write([1, 1, 0], 1)`<br>`db.write(0, "zero")`<br>`db.write("abc", "xyz")`<br>`db.write([0.1, 0.6, 0.8], 1)`|
|Read value by given key or read key/s by given value|`db.read("abc")`<br>`db.read(value="xyz")`<br>`db.read([0.1, 0.6, 0.8])`<br>`db.read(value=1)`|
|Remove key - value pairs by giving key or value|`db.remove({777})`<br>`db.remove(value=0.12)`|
|Get sorted keys (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.keys()`<br>`db.keys("abc")`<br>`db.keys("abc", reverse=True)`|
|Get sorted values (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.values()`<br>`db.values([1, 1, 0])`<br>`db.values([1, 1, 0], reverse=True)`|
|Get a dictionary with key - value pairs as bytes objects (Optionally from specified key)|`db.items()`|
|Close the current database<br>Methods will not work after invoking this function|`db.close()`|
* * *
## Compatibility with **Python3**
* When brainDB is called in python3, it is envoking ubrainDB from micropython version of **unix** to read / write to our database. Basically brainDB uses **subprocess** module to communicate with ubrainDB

### Requirements for Python3 (UNIX)
Run **install.sh**
```shell
git clone https://github.com/schikani/brainDB.git
cd brainDB && ./install.sh
```
### Importing the right module
* Notice the difference in importing the right module for micropython as **ubrainDB** and for python3 as **brainDB** in the example below.
* All the functions are similar both in brainDB and ubrainDB

> ## Python3
```python
from db_scripts import brainDB as DB
db2 = DB("database2")
db.write(1, 89) # key, value to write

```
> ## MicroPython
```python
<<<<<<< HEAD
from db_scripts import ubrainDB as DB
db1 = DB("database1")
db.write(0, 55)
```
=======
# ------------------------------------------------
# Storing 2D / multi-dimensional Arrays
# ------------------------------------------------
>>>>>>> main

* * *

## Examples:
* Storing 2D / multi-dimensional Arrays

```python
from db_scripts import brainDB as DB

database1 = DB("myDB")
database1.verbose(1)

features = [
    [1, 0, 1, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 0]]

labels = [1, 1, 0]

for f, l in zip(features, labels):
    database1.write(f, l)

features_with_label_one = database1.read(value=1)
print(features_with_label_one)
```

<<<<<<< HEAD
* For ESP8266 /  ESP32 auto connections

```python
from db_scripts import ubrainDB as DB
=======
database1.close()


# ------------------------------------------------
# For ESP8266 /  ESP32 auto connections
# ------------------------------------------------

from brainDB import brainDB as DB
>>>>>>> main

credentials = DB(".credentials")

# write ssid and password
credentials.write("ssid", "password")

# more ssids and passwords for multiple locations
credentials.write("ssid4", "password4")
credentials.write("ssid45", "password45")
credentials.write("ssid60", "password60")

credentials.close()

#  ----------Some time later--------------

# Network connection

import network
from brainDB import brainDB as DB

def do_connect():
<<<<<<< HEAD
    from db_scripts import ubrainDB as DB
    import network
    
	credentials = DB(".credentials")
	
=======
  
    credentials = DB("credentials")
    
>>>>>>> main
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        
        # Get keys and values as bytes objects in a dictionary
        dict_B = credentials.items()
        
        print('connecting to network...')
        sta_if.active(True)
        
        for netw in sta_if.scan():
            # catch ssid from index 0 and
            # compare it with the dictionary keys
            if netw[0] in dict_B.keys():
                sta_if.connect(netw[0], dict_B[netw[0]])
  
        while not sta_if.isconnected():
            pass
        credentials.close()
        print('network config:', sta_if.ifconfig())
do_connect()
```
<<<<<<< HEAD
* * *
=======
>>>>>>> main
