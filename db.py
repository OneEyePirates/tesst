import sqlite3
import datetime

def check_db():
    databaseFile = ("database.db")
    db = sqlite3.connect(databaseFile, check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        print("DB was found")
    except sqlite3.OperationalError:
        print("DB was not found")
        cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, reg_date TEXT, last_wallet TEXT)")
        cursor.execute("CREATE TABLE settings(id INTEGER PRIMARY KEY AUTOINCREMENT, check_sub INT)")
        cursor.execute("CREATE TABLE coins(id INTEGER PRIMARY KEY AUTOINCREMENT, name INT, price INT)")
        cursor.execute("INSERT INTO settings(check_sub) VALUES (1)")
        db.commit()
        print("DB was create...")

def get_now_date():
    date = datetime.date.today()
    return date

def get_users_exist(user_id):
    db = sqlite3.connect("database.db", check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
    if cursor.fetchone() is None:
        return False
    else:
        return True

def add_user_to_db(user_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    if not (cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'").fetchone()):
        cursor.execute(f"INSERT INTO users(user_id, reg_date) VALUES ({user_id}, '{get_now_date()}')")
    db.commit()

def get_all_users():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM users")
    row = cursor.fetchall()
    return row

def get_last_wallet(user_id):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT last_wallet FROM users WHERE user_id = '{user_id}'")
    temp = cursor.fetchone()
    if temp[0] is None:
        return False
    else:
        return temp[0]

def set_last_wallet(user_id, text):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET last_wallet = '{text}' WHERE user_id IS '{user_id}'")
    db.commit()

def settings_check_sub():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT check_sub FROM settings")
    res = cursor.fetchone()
    return res[0]

def settings_set_check_sub(num):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE settings SET check_sub = {num}")
    db.commit()

def coins_get_price(name):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT price FROM coins WHERE name = '{name}'")
    res = cursor.fetchone()
    return res[0]

def coins_set_price(name, price):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE coins SET price = {price} WHERE name = '{name}'")
    db.commit()

def get_all_users():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT user_id FROM users""")
    row = cursor.fetchall()
    return row

def get_week_users():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT user_id FROM users WHERE ([reg_date] BETWEEN date('now', '-7 day') AND date('now'))""")
    row = cursor.fetchall()
    return row

def get_all_coins():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT name FROM coins")
    row = cursor.fetchall()
    return row

def coins_create_coin(name):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO coins(name, price) VALUES ('{name}', 1)")
    db.commit()

def coins_delete_coin(name):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM coins WHERE name = '{name}'")
    db.commit()