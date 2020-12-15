import mysql.connector

def createConnection():
    mydb = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database="",
        port=3306
    )
    return mydb

def GetGuilds():
    db = createConnection()
    cur = db.cursor()
    cur.execute("SELECT ID from `guilds`")
    row = [item[0] for item in cur.fetchall()]
    db.close()

    return row

def SetSettings(option, guild, channel):
    db = createConnection()
    cur = db.cursor()
    cur.execute(f"UPDATE `guilds` SET {option} = '{channel}' WHERE ID = {guild}")
    db.commit()
    db.close()

def Enable(guild, mode, type):
    db = createConnection()
    cur = db.cursor()
    cur.execute(f"UPDATE `settings` SET Enabled = {mode} WHERE Guild = {guild} AND Type = {type}")
    db.commit()
    db.close()

def Ignored(guild, data, type):
    db = createConnection()
    cur = db.cursor()
    cur.execute(f"UPDATE `settings` SET Ignored = '{data}' WHERE Guild = {guild} AND Type = {type}")
    db.commit()
    db.close()

def Ratelimit(guild, data, type):
    db = createConnection()
    cur = db.cursor()
    cur.execute(f"UPDATE `settings` SET Ratelimit = '{data}' WHERE Guild = {guild} AND Type = {type}")
    db.commit()
    db.close()

def GetSettings(guild):
    db = createConnection()
    cur = db.cursor()
    query = (f"SELECT Prefix, Language, Channel, ModRoles, IgnoredRoles FROM `guilds` WHERE ID = {guild}")
    cur.execute(query)
    try:
        row = cur.fetchall()
        db.close()
        return row[0]
    except:
        db.close()
        return None

def GetAutoModSettings(guild):
    try:
        db = createConnection()
        cur = db.cursor()

        query = (f"SELECT Type, Enabled, Ratelimit, Ignored FROM `settings` WHERE Guild = {guild}")
        cur.execute(query)
        try:
            row = cur.fetchall()
            db.close()
            return row
        except:
            db.close()
            return None
    except:
        db.close()
        return None

def GetLogs(guild):
    db = createConnection()
    cur = db.cursor()
    query = (f"SELECT Type, Data, Timestamp FROM `logs` WHERE Guild = {guild} ORDER BY Timestamp DESC LIMIT 100")
    cur.execute(query)
    try:
        row = cur.fetchall()
        db.close()
        return row
    except:
        db.close()
        return None

def AddRule(guild, type, infractions, duration, increment):
    db = createConnection()
    cur = db.cursor()
    try:
        cur.execute(f"INSERT INTO `rules` (Guild, Type, Infractions, Duration, Increment) VALUES ('{guild}', '{type}', '{infractions}', '{duration}', '{increment}')")
        db.commit()
        db.close()
    except:
        db.close()
        return

def DeleteRule(guild, type):
    db = createConnection()
    cur = db.cursor()
    try:
        cur.execute(f"DELETE FROM `rules` WHERE Guild = {guild} AND Type = {type}")
        db.commit()
        db.close()
    except:
        db.close()
        return

def GetRules(guild):
    db = createConnection()
    cur = db.cursor()
    query = (f"SELECT Type, Infractions, Duration, Increment FROM `rules` WHERE Guild = {guild} ORDER BY ID ASC")
    cur.execute(query)
    try:
        row = cur.fetchall()
        db.close()
        return row
    except:
        db.close()
        return None