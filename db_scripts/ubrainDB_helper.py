from ubrainDB import ubrainDB as DB
from sys import argv
import json

with open('./db_scripts/commands.json') as c:
    c = json.load(c)

COMMANDS = c["COMMANDS"]

CLOSE = argv[1]
VERBOSE = argv[2]
DB_NAME = argv[3]
ARG_COMMAND = argv[4]
ARGS = argv[5:]


def database():
    db = DB(DB_NAME)
    db.verbose(int(VERBOSE))
    if int(CLOSE) == 1:
        print(db.close(int(CLOSE)))
    else:
        db.close(CLOSE)
    return db


def action_on_commands():
    db = database()

    if ARG_COMMAND == COMMANDS[0]:
        print(db.write(ARGS[0], ARGS[1]))

    elif ARG_COMMAND == COMMANDS[1]:
        print(db.read(ARGS[0]))

    elif ARG_COMMAND == COMMANDS[2]:
        print(db.read(value=ARGS[0]))

    elif ARG_COMMAND == COMMANDS[3]:
        print(db.remove(ARGS[0]))

    elif ARG_COMMAND == COMMANDS[4]:
        print(db.remove(value=ARGS[0]))

    elif ARG_COMMAND == COMMANDS[5]:
        print(db.keys())

    elif ARG_COMMAND == COMMANDS[6]:
        print(db.keys(reverse=True))

    elif ARG_COMMAND == COMMANDS[7]:
        print(db.keys(start_key=ARGS[0]))

    elif ARG_COMMAND == COMMANDS[8]:
        print(db.keys(start_key=ARGS[0], reverse=True))

    elif ARG_COMMAND == COMMANDS[9]:
        print(db.values())

    elif ARG_COMMAND == COMMANDS[10]:
        print(db.values(reverse=True))

    elif ARG_COMMAND == COMMANDS[11]:
        print(db.values(start_key=ARGS[0]))

    elif ARG_COMMAND == COMMANDS[12]:
        print(db.values(start_key=ARGS[0], reverse=True))

    elif ARG_COMMAND == COMMANDS[13]:
        print(db.items())

    elif ARG_COMMAND == COMMANDS[14]:
        print(db.items(start_key=ARGS[0]))

    elif ARG_COMMAND == COMMANDS[15]:
        print(db.databases())

    elif ARG_COMMAND == COMMANDS[16]:
        print(db.close())


action_on_commands()
