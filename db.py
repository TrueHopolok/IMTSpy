DB_PATH = 'main.db'
SALT_SIZE = 20
SALT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


import random
import argon2
import base64
import sqlite3


logined_user_id = None


class Error():
    def __init__(self, __status : int = 0, __message : str = ''):
        self.message = __message
        self.status = __status
    def __str__(self) -> str:
        return self.message


def generate_salt() -> bytes:
    return str().join([random.choice(SALT_ALPHABET) for _ in range(SALT_SIZE)]).encode()


def user_insert(username : str, password : str) -> None | Error:
    # name validation
    if len(username) < 3:
        return Error(101, '<username> value was invalid : too short')
    if not username.isprintable():
        return Error(101, '<username> value was invalid : not printable')
    
    # password validation
    if len(password) < 8:
        return Error(102, '<password> value was invalid : too short') 

    # db connection
    con = sqlite3.connect(DB_PATH, autocommit=True)

    # name uniqness verification
    cur = con.execute("""
    SELECT username FROM users
    WHERE username=?;
    """, (username,))
    if not (cur.fetchone() is None):
        con.close()
        return Error(201, '<username> value was invalid : already exist')

    # password encryption
    salt = generate_salt()
    hash = argon2.hash_password(password.encode(), salt)

    # db insertion
    con.execute("""
    INSERT INTO users (username, password)
    VALUES (?, ?);
    """, (username, base64.encodebytes(hash)))
    con.close()

    return None


def user_login(username : str, password : str) -> None | Error:
    global logined_user_id

    # db selection by uesrname
    con = sqlite3.connect(DB_PATH, autocommit=True)
    res = con.execute("""
    SELECT id, username, password FROM users
    WHERE username = ?;
    """, (username,)).fetchone()
    con.close()
    if not res:
        return Error(101, '<username> value was invalid : user not found')
    
    # password verification
    try:
        argon2.verify_password(base64.decodebytes(res[2]), password.encode())
    except argon2.exceptions.VerifyMismatchError:
        return Error(102, '<password> value was invalid : password is incorrect')
    
    logined_user_id = res[0]
    return None
    

def user_logout():
    global logined_user_id
    logined_user_id = None


def item_insert(name : str, description : str) -> None | Error:
    global logined_user_id

    # login validation
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 

    # name validation
    if not name.isprintable():
        return Error(101, '<name> value was invalid : value is not printable')

    # db insertion
    con = sqlite3.connect(DB_PATH, autocommit=True)
    con.execute("""
    INSERT INTO items (name, description)
    VALUES (?, ?);
    """, (name, description))
    con.close()

    return None


def item_get(fieldname : str, fieldvalue) -> list | Error:
    global logined_user_id

    # login validation
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 
    
    if fieldname == 'all':
        con = sqlite3.connect(DB_PATH, autocommit=True)
        res = con.execute(f"""
        SELECT * FROM items;
        """).fetchall()
        con.close()
        return res

    # fieldname & fieldvalue validation
    if fieldname == 'id' or fieldname == 'last_user_id' or fieldname == 'current_user_id':
        if not isinstance(fieldvalue, int):
            return Error(101, '<fieldvalue> value was invalid : invalid type')
    elif fieldname == 'name':
        if not isinstance(fieldvalue, str):
            return Error(101, '<fieldvalue> value was invalid : invalid type')
    else:
        return Error(102, '<fieldname> value was invalid : such field does not exist')
    
    # db selection by given args
    con = sqlite3.connect(DB_PATH, autocommit=True)
    res = con.execute(f"""
    SELECT * FROM items
    WHERE {fieldname} = ?;
    """, (fieldvalue,)).fetchall()
    con.close()
    return res


def item_update(id : int, name : str | None = None, description : str | None = None) -> None | Error: 
    global logined_user_id

    # login validation
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 

    # id validation
    con = sqlite3.connect(DB_PATH, autocommit=True)
    data = con.execute("""
    SELECT * FROM items
    WHERE id=?;
    """, (id,)).fetchone()
    if data == None:
        con.close()
        return Error(101, '<id> value was invalid : no item with such id exist')
    
    # data replacement
    data = [data[1], data[2]]
    if name != None:
        if not name.isprintable():
            con.close()
            return Error(102, '<name> value was invalid : value is not printable')
        data[0] = name
    if description != None:
        data[1] = description
    
    # db update
    con.execute("""
    UPDATE items
    SET name = ?, description = ?
    WHERE id = ?;
    """, (data[0], data[1], id))
    con.close()

    return None


def item_remove(id : int) -> None | Error:
    global logined_user_id

    # login validation  
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 
    
    # db removal
    con = sqlite3.connect(DB_PATH, autocommit=True)
    con.execute("""
    DELETE FROM items 
    WHERE id = ?;
    """, (id,))
    con.close()


def item_book(id : int, unbook : bool = False) -> None | Error:
    global con
    global logined_user_id

    # login validation
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 
    
    # id validation
    con = sqlite3.connect(DB_PATH, autocommit=True)
    data = con.execute("""
    SELECT * FROM items
    WHERE id=?;
    """, (id,)).fetchone()
    if data == None:
        con.close()
        return Error(101, '<id> value was invalid : no item with such id exist')
    
    # data update and validation
    if data[4] == logined_user_id and not unbook:
        return Error(202, '<current_id> and <login_id> are same : can not be changed to same id')
    data = [data[3], data[4], data[5]]
    data[0] += 1
    data[2] = data[1]
    if unbook:
        data[1] = None
    else:
        data[1] = logined_user_id

    # db update
    con.execute("""
    UPDATE items
    SET user_count = ?, current_user_id = ?, last_user_id = ?
    WHERE id = ?;      
    """, (data[0], data[1], data[2], id))
    con.close()

    return None


def total_clear():
    global logined_user_id

    # login validation
    if not logined_user_id:
        return Error(201, '<login_id> value was invalid : None') 

    # data base clear
    con = sqlite3.connect(DB_PATH, autocommit=True)
    con.execute("""
    DELETE FROM items;
    """)
    con.execute("""
    DELETE FROM users;
    """)
    con.close()


if __name__ == '__main__':
    print("\ndb.py was executed\n")