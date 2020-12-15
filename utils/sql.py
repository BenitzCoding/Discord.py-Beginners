import mysql.connector
import datetime
import json
from collections import namedtuple


def fetch(file):
    try:
        with open(file, encoding="utf8") as data:
            return json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")


config = fetch("utils/cfg.json")


def createConnection():
    mydb = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_pass,
        database=config.mysql_db,
        port=config.mysql_port
    )
    return mydb


def Fetch(Table, Row, Value):
    mydb = createConnection()
    cur = mydb.cursor()
    query = (f"SELECT {Row} FROM {Table} WHERE ID = {Value}")
    cur.execute(query)
    row = cur.fetchone()
    mydb.close()
    if row:
        return row[0]


# Caching

def Cache(Guild):
    Settings = {
        "Prefix": None,
        "Language": None,
        "Logs": None,
        "ModRoles": None,
        "IgnoredRoles": None,
        "AutoMod": {},
        "Rules": []
                }
    mydb = createConnection()
    cur = mydb.cursor()
    try:
        cur.execute(f"SELECT Prefix, Channel, Language, ModRoles, IgnoredRoles FROM `guilds` WHERE ID = {Guild}")
        data = cur.fetchall()[0]
        Settings["Prefix"] = data[0]
        Settings["Logs"] = data[1]
        Settings["Language"] = data[2] - 1
        Settings["ModRoles"] = data[3]
        Settings["IgnoredRoles"] = data[4]
    except:
        pass

    try:
        cur.execute(f"SELECT Type, Enabled, Ratelimit, Ignored FROM `settings` WHERE Guild={Guild} ORDER BY Type ASC")
        data = cur.fetchall()


        for i in data:
            Settings["AutoMod"][i[0]] = {"Enabled": i[1], "Ratelimit": i[2], "Ignored": i[3]}
    except:
        pass

    try:
        cur.execute(f"SELECT Type, Infractions, Duration, Increment from `rules` WHERE Guild={Guild} ORDER BY Type ASC")
        data = cur.fetchall()

        for i in data:
            Settings["Rules"].append([i[0], i[1], i[2], i[3]])
    except:
        pass

    mydb.close()

    return Settings

# Adding Guilds to all tables

def AddData(ID):
    mydb = createConnection()
    cur = mydb.cursor()
    queries = [
        f"INSERT INTO `guilds` (ID) VALUES ('{ID}')",
        f"INSERT INTO `captcha` (ID) VALUES ('{ID}')"
    ]

    for query in queries:
        try:
            cur.execute(query)
        except:
            pass
    try:
        for type in range(1, 11):
            cur.execute(f"INSERT INTO `settings` (Guild, Type) VALUES ('{ID}', '{type}')")
        mydb.commit()
    except:
        pass

    mydb.close()

def RemoveData(ID):
    mydb = createConnection()
    cur = mydb.cursor()

    queries = [
        f"DELETE FROM `guilds` WHERE ID = {ID}",
        f"DELETE FROM `settings` WHERE Guild = {id}",
        f"DELETE FROM `captcha` WHERE Guild = {id}",
        f"DELETE FROM `logs` WHERE Guild = {id}",
        f"DELETE FROM `rules` WHERE Guild = {id}",
        f"DELETE FROM `infractions` WHERE Guild = {id}"
    ]
    for query in queries:
        try:
            cur.execute(query)
        except:
            pass

    mydb.close()


# Logging Table

def LogMe(ID, Type, Log):
    mydb = createConnection()
    try:
        cur = mydb.cursor()
        Log = Log.replace('"', '').replace("'", "")
        cur.execute(
            f"INSERT INTO `logs` (Guild, type, Data, Timestamp) VALUES('{ID}', {int(Type)}, '{Log}', '{datetime.datetime.now()}')")
        mydb.commit()
    except:
        return
    finally:
        mydb.close()

# Warnings

def Warn(Guild, User, Invoker, Reason):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(
        f"INSERT INTO `infractions` (Guild, User, Invoker, Reason, Timestamp) VALUES({Guild}, {User}, {Invoker}, '{Reason}', '{datetime.datetime.now()}')")
    mydb.commit()
    mydb.close()

def GetInfractions(Guild, User):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"SELECT * FROM `infractions` WHERE Guild = {Guild} AND User = {User}")
    try:
        row = cur.fetchall()
        return row
    except:
        return None
    finally:
        mydb.close()

def RemoveInfraction(ID, Guild, User):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"SELECT * FROM `infractions` WHERE Guild = {Guild} AND User = {User} AND ID = {ID}")
    try:
        row = cur.fetchone()
    except:
        return None
    else:
        if row:
            cur.execute(f"DELETE from `infractions` WHERE Guild = {Guild} AND User = {User} AND ID = {ID}")
            mydb.commit()
            return True
    finally:
        mydb.close()

# Data Request

def GetData(ID):
    mydb = createConnection()
    cur = mydb.cursor()
    query = (f"SELECT * FROM `infractions` WHERE User = {ID} OR Invoker = {ID}")
    cur.execute(query)
    try:
        row = cur.fetchall()
        for i in row:
            with open(f"{ID}-datarequest.txt", "a") as myfile:
                myfile.write(
                    "GuildID: {} | UserID: {} | Invoker: {} | Reason: {} | Date: {}\n".format(i[1], i[2], i[3], i[4],
                                                                                              i[5]))
                myfile.close()
    except:
        pass
    finally:
        mydb.close()

# Rules

def GetInfractionsAfter(user, guild, after):
    mydb = createConnection()
    cur = mydb.cursor()
    cur.execute(f"SELECT COUNT(*) from `infractions` WHERE Guild = {guild} AND User = {user} AND Timestamp > '{after}'")
    try:
        row = cur.fetchone()
        return row[0]
    except:
        return
    finally:
        mydb.close()
