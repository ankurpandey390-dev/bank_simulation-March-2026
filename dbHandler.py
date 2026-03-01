import sqlite3

def create_table():
    conobj=sqlite3.connect(database="bank.sqlite3")
    curobj=conobj.cursor()
    query='''create table if not exists accounts(
    acn integer primary key autoincrement,
    name text,
    pass text,
    email text,
    mob text,
    adhar text,
    bal float,
    opendate datetime
    )
'''
    curobj.execute(query)
    conobj.close()
    print("table created or already exists")
