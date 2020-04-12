# This Python file uses the following encoding: utf-8

import json
from tinydb import TinyDB, Query

db = TinyDB('db/db.json')


def allNotes():
    Notes = Query()
    return db.search(Notes.note.exists())


def save(config, data):
    if type(data) is dict:
        db.insert(data)
    elif type(data) is str:
        db.insert(json.loads(data))
    else:
        log(config).warn("Unknown data type.")

    return


def close_db():
    db.close()
    return


def log(config):
    return config.get("ROOT_LOGGER").getChild(__name__)
