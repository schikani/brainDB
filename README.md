# brainDB
![alt text](https://github.com/schikani/brainDB/blob/main/brainDB.png)

## About:
* This project is based on the btree module from [MicroPython](https://github.com/micropython/micropython) which is based on [BerkelyDB](https://www.oracle.com/database/technologies/related/berkeleydb.html) library.
* Btrees are efficient in retrieving values from given keys. Both keys and values are stored in bytes objects.
* Micropython datatypes like: **int, float, str, list, tuple, set, dict, bytes, bytearray, bool** can be used both as keys and values for the brainDB database.
* brainDB is compatible with any device running MicroPython with btree module in it like: **ESP8266, ESP32, Unix etc.**
  <br>
## Possible use cases:
* Data Logging from sensors.
* Storing Wifi credentials in ESP8266 / ESP32 boards.
* Because brainDB is compatible with Unix systems, it is possible to use the Unix version of MicroPython to create the database for later use in micro-controller versions.
* Can be used to store datasets efficiently for training Machine Learning models as well as storing weights, biases etc for using it in future predictions.
  <br>
## class brainDB:
|Use|Function
|-|-|
|Create a new database by giving it a name<br>"someName" file is created inside "DB" folder if it doesn't exist. The path can be changed in "brainDB.py"|`db = DB("someName")`|
|Get the names of all the databases in a list|`db.databases()`|
|Set verbose (default is set to 0)<br>If set to 1, it displays information while writing / removing in the database|`db.verbose(1)`|
|Write key - value pairs to the current database. The first argument is key and second is value|`db.write({777}, 0.12)`<br>`db.write([1, 1, 0], 1)`<br>`db.write(0, "zero")`<br>`db.write("abc", "xyz")`<br>`db.write([0.1, 0.6, 0.8], 1)`|
||`db.get_items()`|
|Read value by given key or read key/s by given value|`db.read("abc")`<br>`db.read(value="xyz")`<br>`db.read([0.1, 0.6, 0.8])`<br>`db.read(value=1)`|
|Remove key - value pairs by giving key or value|`db.remove({777})`<br>`db.remove(value=0.12)`|
|Get sorted keys (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.sorted_keys()`<br>`db.sorted_keys("abc")`<br>`db.sorted_keys("abc", reverse=True)`|
|Get sorted values (Optionally from specified key)<br>Also reverse can be set to True to get the list in reverse order|`db.sorted_values()`<br>`db.sorted_values([1, 1, 0])`<br>`db.sorted_values([1, 1, 0], reverse=True)`|
|Get a dictionary with key - value pairs as bytes objects (Optionally from specified key)|`db.get_items()`|
|Close the current database<br>Methods will not work after invoking this function|`db.close()`|

## Examples:
```python
# ------------------------------------------------
# Storing 2D / multi-dimensional Arrays
# ------------------------------------------------

from brainDB import brainDB as DB

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


# ------------------------------------------------
# For ESP8266 /  ESP32 auto connections
# ------------------------------------------------

from brainDB import brainDB as DB

credentials = DB("credentials")

# write ssid and password
credentials.write(key="ssid", value="password")

# more ssids and passwords for multiple locations
credentials.write(key="ssid4", value="password4")
credentials.write(key="ssid45", value="password45")
credentials.write(key="ssid60", value="password60")

credentials.close()

#  ----------Some time later--------------

# Network connection

import network
from brainDB import brainDB as DB

def do_connect():
  
    credentials = DB("credentials")
    
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        
        # Get keys and values as bytes objects in a dictionary
        dict_B = credentials.get_items()
        
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
<br>

## Note:
* It is better to distribute the values with more keys **OR**, distribute data across different databases. This can prevent file corruption.
