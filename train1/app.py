from flask import Flask, render_template

app = Flask(__name__)

#flask定义路由通过装饰器实现
@app.route('/',methods=['GET','POST'])#路由默认支持GET，单独增加POST

def hello_world():
    return render_template('1.html')

#<>定义路由参数
#路由访问优化,int类型
@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    #参数类型默认是字符串
    #需要在视图函数（）内填入参数名
    return 'order_id %s' % order_id

if __name__ == '__main__':
    app.run(debug=True)
