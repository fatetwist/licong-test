from flask import Flask,render_template,redirect,url_for,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required
import json
import ncudenglu as ylogin
import library as lib

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='a not found key'
class loginform(Form):
    username = StringField('学号',validators=[Required()])
    password = PasswordField('密码',validators=[Required()])
    form_submit = SubmitField('登录')

class searchform(Form):
    key = StringField('输入关键词',validators=[Required()])
    form_submit = SubmitField('搜索')





@app.route('/login/',methods=['POST','GET'])
def ulogin():

    form_login = loginform()
    form_search = searchform()



    if form_login.validate_on_submit():
        res_login = ylogin.login(form_login.username.data,form_login.password.data)
        print(res_login)
        if  res_login != 'unknownerror':

            my_info = ylogin.get_info(res_login['token'])
            session['my_info'] = json.dumps(my_info)

            return redirect(url_for('ulib'))

        else:

            session['pass_message']='用户名或密码错误'

            return redirect(url_for('ulogin'))
    try:
        pass_message = session['pass_message']
        session['pass_message']=''

        return render_template('login.html', form=form_login, pass_message=pass_message)
    except:
        return render_template('login.html', form=form_login)


@app.route('/lib/',methods=['POST','GET'])
def ulib():
    form_search = searchform()
    my_info = json.loads(session['my_info'])

    if form_search.validate_on_submit():
        session['result_key'] = form_search.key.data


        return redirect(url_for('uresult'))
    return render_template('lib.html',form=form_search,my_info=my_info)


@app.route('/')
def uindex():
    return redirect(url_for('ulogin'))

@app.route('/result/')
def uresult():
    key = session['result_key']
    print('ok1===')
    result = lib.getcatalog(key)
    print(result)
    return render_template('result.html',key = key,result = result)


if __name__=='__main__':
    app.run()
