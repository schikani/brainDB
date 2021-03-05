from db_scripts import ubrainDB as DB
import sys

db = DB("upy_test")

version = sys.version
implementation = sys.implementation[0]
mpy = sys.implementation[2]
platform = sys.platform

db.write(0, "-" * 60)
db.write(1, "* This message is displayed from {} *".format("./DB/upy_test.brain"))
db.write(2, "-" * 60)
db.write(3, "MicroPythonVersion: {}".format(version))
db.write(4, "Implementation: {}".format(implementation))
db.write(5, "MPY: {}".format(mpy))
db.write(6, "Platform: {}".format(platform))
db.write(7, "-" * 60)

for i in range(8):
    print(db.read(i))
