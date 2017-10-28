from flask import Flask,render_template
from flask_bootstrap import Bootstrap
# form
from flask_wtf import Form
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Required
import sqlite3

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='GUOKAOHE'
class newform(Form):
    content = TextAreaField('please enter you message:',validators=[Required()],  render_kw={'placeholder':'Message board','style':'background: url("arrow.ico");height:500;'})
    form_submit = SubmitField('Submit')


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

@app.route('/',methods=['GET','POST'])
def index():
    subform = newform()
    if subform.validate_on_submit():
# get num,mboard
        conn = sqlite3.connect('mboard.db')
        cu = conn.cursor()
        num = get_count(cu,'catalog')+1
        mboard = subform.content.data
# get time
        time_now = get_time()
# insert and commit db
        cu.execute("insert into catalog values (?,?,?)", (num, time_now, mboard))
        conn.commit()
# get message  then  return
        cu.execute('select * from catalog')
        message = cu.fetchall()

        num = len(message)
        num_list = list(range(num-1,-1,-1))
#        print('===========>>>>',num_list)
#        print('===========>>>>',message)
        conn.close()
        return render_template('mboard.html',message=message,subform=subform,num_list =num_list)
    conn = sqlite3.connect('mboard.db')
    cu = conn.cursor()
    cu.execute('select * from catalog')
    message = cu.fetchall()
    num = len(message)
    conn.close()
    num_list = list(range(num-1,-1,-1))


    return render_template('mboard.html',message=message,subform=subform,num_list =num_list)



   


if __name__ == '__main__':
    app.run()
