

from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo


app = Flask(__name__)
app.secret_key='qwertyuiopasdfghjkzxcvbnm,.;[]1234567890-='

#flask定义路由通过装饰器实现
@app.route('/',methods=['GET','POST'])#路由默认支持GET，单独增加POST


class LoginForm(FlaskForm):
    username=StringField('用户名:',validators=[DataRequired()])
    password=PasswordField('密码:',validators=[DataRequired()])
    password2=PasswordField('确认密码:',validators=[DataRequired(),EqualTo('password','密码填入的不一致')])
    submit=SubmitField('提交')

@app.route('/form',methods=['GET','POST'])
def login():
    login_form=LoginForm()

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        password2=request.form.get('password2')

        #WTF验证逻辑
        if login_form.validate_on_submit():
            print(username,password)
            return 'success'
        else:
            flash('False Parameter')

    return render_template('2.html',form=login_form)
#request请求对象-->获取请求方式和请求数据
#给模板html传递消息用flash
def index():
    #1.判断请求方式
    if request.method=='POST':
        # 2.获取请求参数
        username=request.form.get('username')
        password=request.form.get('password')
        password2=request.form.get('password2')

        # 3.验证
        if not all([username,password,password2]):
            flash(u"参数不完整")#flash闪现消息需要加密,设置secret_key，加密消息
        elif password != password2:
            flash(u"密码不一致")
        else:
            return 'success'


    return render_template('2.html')

if __name__ == '__main__':
    app.run(debug=True)
