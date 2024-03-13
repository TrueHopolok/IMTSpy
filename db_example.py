import db

####
#### users test
####

e = db.user_insert('test', 'password')
if e: print(e)
else: print("user: created")

e = db.user_login('test', 'password')
if e: print(e)
else: print("user: logined")

e = db.user_login('test', 'notpassword')
if e: print(e)
else: print("user: logined")

e = db.user_login('nottest', 'password')
if e: print(e)
else: print("user: logined")

# db.logout()
# print("user: logouted")

####
#### items test
####

e = db.item_insert('rubic cube', 'just some puzzle')
if e: print(e)
else: print("item: added")

e = db.item_get(fieldvalue='rubic cube', fieldname='name')
if isinstance(e, db.Error): print(e)
# else: print(e) # print list
else: print("item: found")

e = db.item_update(21, name='poker galds')
if e: print(e)
else: print("item: updated")

e = db.item_book(24)
if e: print(e)
else: print("item: booked")

e = db.item_book(24, unbook=True)
if e: print(e)
else: print("item: unbooked")

e = db.item_remove(22)
if e: print(e)
else: print("item: removed")

####
#### db clear
####

# db.total_clear()
# print("database fully cleared")