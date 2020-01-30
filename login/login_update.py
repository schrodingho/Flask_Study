
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)


@app.route('/article')
def article():
    return render_template('more.html')

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
            return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        if not account or not password:
            return "<script> alert('账号和密码不能为空') </script>"+render_template('login.html')
        elif password!='123456':
            return "<script> alert('账号或者密码错误，请重新输入') </script>"+render_template('login.html')
        else:
            return redirect(url_for('article'))