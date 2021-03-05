from db_scripts import brainDB as DB
import platform
import sys

db = DB("py_test")

pyVersion = sys.version.split('\n')[0]
system = platform.system()
machine = platform.machine()
platform = platform.platform()

db.write(0, "-" * 60)
db.write(1, "* This message is displayed from {} *".format("./DB/py_test.brain"))
db.write(2, "-" * 60)
db.write(3, "Python3Version: {}".format(pyVersion))
db.write(4, "System: {}".format(system))
db.write(5, "Machine: {}".format(machine))
db.write(6, "Platform: {}".format(platform))
db.write(7, "-" * 60)

for i in range(8):
    print(db.read(i))
