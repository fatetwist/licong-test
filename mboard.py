# coding=utf-8
from flask import Flask,render_template,session,redirect,url_for
from flask_bootstrap import Bootstrap
# form
from flask_wtf import Form
from wtforms import TextAreaField,SubmitField,PasswordField
from wtforms.validators import Required
import sqlite3
import dbcon

dbcon.connect('mboard.db')
file = r'mboard.db'
app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='GUOKAOHE'
class newform(Form):
    content = TextAreaField('please enter you message:',validators=[Required()],  render_kw={'placeholder':'Message board','style':'background: url("arrow.ico");height:500;'})
    form_submit = SubmitField('Submit')
class loginform(Form):
    pwd = PasswordField(u'你真不简单，居然可以找到这！\n ok,Please enter your password')
    form_submit = SubmitField(u'进入留言板')





@app.route('/login/',methods=['GET','POST'])
def login():
    conn = sqlite3.connect(file)
    cu = conn.cursor()
    rcnz = session.get('rcnz')
    try:
        cu.execute('select * from users where pwd=\'%s\' ' % rcnz)
        if len(cu.fetchall()) > 0:
            conn.close()
            return redirect(url_for('mboard'))
    except sqlite3.OperationalError:

        pass



    form_login = loginform()
    if form_login.validate_on_submit():

        cu.execute('select * from users where pwd=\'%s\'' % form_login.pwd.data)
        r = cu.fetchall()
        if len(r) > 0:
            conn.close()
            session['rcnz'] = form_login.pwd.data
            session['name'] = r[0][0]
            return redirect(url_for('mboard'))
        else:
            conn.close()
            session['message'] = u'密码错误，若你是外来人员请不要反复尝试，否则你们的浏览器将会崩溃！'
            return redirect(url_for('login'))


    conn.close()
    form_login = loginform()
    error = session.get('message')
    return render_template('login.html',form_login = form_login,error = error)

@app.route('/')
def index():

    return redirect(url_for('login'))

@app.route('/520',methods=['GET','POST'])
def mboard():
    rcnz = session.get('rcnz')
    subform = newform()
    conn = sqlite3.connect(file)
    cu = conn.cursor()
    try:
        cu.execute('select * from users where pwd="%s"' % rcnz)

        if len(cu.fetchall()) < 1:
            conn.close()
            return redirect(url_for('login'))
    except sqlite3.OperationalError:
        return redirect(url_for('login'))
        pass



    if subform.validate_on_submit():
        name  = session.get('name')

        cu.execute('select * from catalog')
        all = cu.fetchall()
        if len(all) >0:
            num = all[-1][0]+1
        else:
            num = 1
        print(num)
        time_now = get_time()
        mboard = subform.content.data


        cu.execute("insert into catalog values (?,?,?,?)" , (num, time_now, mboard,name))
        conn.commit()

        cu.execute('select * from catalog')
        message = cu.fetchall()

        num = len(message)
        num_list = list(range(num-1,-1,-1))
        conn.close()
        return redirect(url_for('mboard'))

    cu.execute('select * from catalog')
    message = cu.fetchall()
    num = len(message)
    conn.close()
    num_list = list(range(num-1,-1,-1))
    name = session.get('name')


    return render_template('mboard.html',message=message,subform=subform,num_list =num_list,name=name,num=num)

@app.route('/dbdelete/<id>')
def deleteMessage(id):
    if islogin() ==True:
        dbcon.delete('catalog',int(id))
        return '删除成功  '+id
    else:
        return '未认证'


def get_count(db_cursor,db_table):
    db_cursor.execute('select * from %s' % db_table)
    db_list = db_cursor.fetchall()
    return len(db_list)
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
def match_rcnz(rcnz,pwds):
    for x in pwds:
        if x == rcnz:
            return True
        else:
            return False

def make_shell_context():
    return dict(app=app,db=db)
def islogin():
    rcnz = session.get('rcnz')
    if not rcnz:
        return False

    cu = dbcon.cu
    cu.execute('select * from users where pwd=%s' % str(rcnz))

    if len(cu.fetchall()) >0:
        return True
    else:
        return False







if __name__ == '__main__':
    app.run()
