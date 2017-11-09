import sqlite3

conn = None
cu = None


def connect(URI):
    global conn,cu
    conn = sqlite3.connect(URI)
    cu = conn.cursor()
    

def delete(table,id):
    if conn==None or cu==None:
        return
    cu.execute('delete from %s where id=%s' % (table,id))
    conn.commit()

def dbclose():
    conn.close()
