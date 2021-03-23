# brainDB
![alt text](https://github.com/schikani/brainDB/blob/main/brainDB.png)

## About:
* This project is based on the btree module from [MicroPython](https://github.com/micropython/micropython) which is based on [BerkelyDB](https://www.oracle.com/database/technologies/related/berkeleydb.html) library.
* Btrees are efficient in retrieving values from given keys. Both keys and values are stored in bytes objects.
* Python datatypes like: **int, float, str, list, tuple, set, dict, bytes, bytearray, bool** can be used both as keys and values for the database.
<<<<<<< HEAD
* brainDB is compatible with both **cpython** and **micropython**
* Because of this compatibility, it is possible to create the database in native system python for later use in micropython versions of micro-controllers. 

## Easy of use:
`db = DB("databaseName")`
`db.write(key, value)`
`db.read(key)` OR `db.read(value=value)`

=======
* brainDB is compatible with **python3** and **micropython**
* Because brainDB package is compatible with python3, it is possible to create the database for later use in micropython versions of micro-controllers.
>>>>>>> 8b2c7fe355c908bcae568202b945202cbd806b08
## Possible use cases:
* Data Logging from sensors.
* Storing Wifi credentials in ESP8266 / ESP32 boards.
* Can be used to store datasets efficiently for training Machine Learning models as well as storing weights, biases etc for using it in future predictions.
* Everywhere when data needs to be stored and accessed by key
* * *
## class brainDB / ubrainDB:
|Use|Function
|-|-|
|Create a new database by giving it a name<br>The database file is created inside "DB" folder if it doesn't exist. The path can be changed in "ubrainDB.py"|`db = DB("someName")`<br>`db2 = DB("anotherName")`|
|Get the names of all the databases in a list|`db.databases()`|
|Set verbose (default is set to 0)<br>If set to 1, it displays information while writing / removing in the database|`db.verbose(1)`|
|Write key - value pairs to the current database. The first argument is key and second is value|`db.write({777}, 0.12)`<br>`db.write([1, 1, 0], 1)`<br>`db.write(0, "zero")`<br>`db.write("abc", "xyz")`<br>`db.write([0.1, 0.6, 0.8], 1)`|
|Read value by given key or read key/s by given value|`db.read("abc")`<br>`db.read(value="xyz")`<br>`db.read([0.1, 0.6, 0.8])`<br>`db.read(value=1)`|
|Remove key - value pairs by giving key or value|`db.remove({777})`<br>`db.remove(value=0.12)`|
|Get sorted keys (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.keys()`<br>`db.keys("abc")`<br>`db.keys("abc", reverse=True)`|
|Get sorted values (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.values()`<br>`db.values([1, 1, 0])`<br>`db.values([1, 1, 0], reverse=True)`|
|Get a dictionary with key - value pairs as bytes objects (Optionally from specified key)|`db.items()`|
|Remove a database by it's name. If the current database is selected, it will be erased of all items.|`db.remove_database("someName")`|
|Close the current database<br>Read / Write methods will not work after invoking this function|`db.close()`|
|It reopens a database after it was closed<br>Read / Write methods will work again |`db.reopen()`|
* * *
## Compatibility with **CPython**
* As I started working on brainDB, it was written only for micropython. But with the help of subprocess module, I made a wrapper around MicroPython to use the script in CPython.
* When brainDB is called in cpython, it is envoking ubrainDB from micropython version of **unix** to read / write to our database. Basically brainDB uses **subprocess** module to communicate with ubrainDB

### Requirements for CPython (UNIX)
Run **install.sh**
```shell
git clone https://github.com/schikani/brainDB.git
cd brainDB && ./install.sh
```
### Importing the right module
* Notice the difference in importing the right module for micropython as **ubrainDB** and for cpython as **brainDB** in the example below.
* All the functions are similar both in brainDB and ubrainDB

> ## CPython
```python
from db_scripts import brainDB as DB
db1 = DB("database1")
db1.write(1, 89) # key, value to write

```
> ## MicroPython
```python
from db_scripts import ubrainDB as DB
db2 = DB("database2")
db2.write(0, 55)
```
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
database1.close()
```
* For ESP8266 /  ESP32 auto connections

```python
from db_scripts import ubrainDB as DB

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

def do_connect():

    from db_scripts import ubrainDB as DB
    import network
  
    credentials = DB(".credentials")
    
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

* * *

