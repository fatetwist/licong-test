import sqlite3

conn = None
cu = None

def get_time():
    import time
    t =time.localtime()
    y = t.tm_year
    mon = t.tm_mon
    d = t.tm_mday
    h = t.tm_hour
    min = t.tm_min
    s = t.tm_sec
    if mon < 10:
        mon='0'+str(mon)
    if d < 10 :
        d='0'+str(d)
    if h < 10:
        h = '0' + str(h)
    if min < 10:
        min = '0'+str(min)
    if s < 10:
        s = '0' + str(s)
    return '%s.%s.%s  %s:%s:%s' % (y,mon,d,h,min,s)

def connect(URI):
    global conn,cu
    conn = sqlite3.connect(URI)
    cu = conn.cursor()
    

def delete(table,id):
    if conn==None or cu==None:
        return
    cu.execute('delete from %s where id=%s' % (table,id))
    conn.commit()
def close():
    conn.close()

def submit(table,user,content):
    if conn==None or cu==None:
        return

    try:
        cu.execute("select * from %s" % table)
        db_res = cu.fetchall()
        if len(db_res)>0:
            id = db_res[-1][0] + 1
        else:
            id=1

        time = get_time()
        cu.execute("insert into %s values(%s,'%s','%s','%s')" % (table, id, time, content, user))
        conn.commit()
        return True


    except BaseException as e:
        print(e)
        return False


def getMessage():
    cu.execute('select * from catalog')
    db_res = cu.fetchall()
    ms = []
    # 编号 时间 内容 姓名
    for x in db_res:
        id = x[0]
        time = x[1]
        content = x[2]
        name = x[3]
        a={'id':id,'time':time,'content':content,'name':name}
        ms.append(a)
    return ms