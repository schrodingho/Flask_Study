from flask import Flask, render_template

app = Flask(__name__)

#flask定义路由通过装饰器实现
@app.route('/',methods=['GET','POST'])#路由默认支持GET，单独增加POST
def hello_world():
    url_str="www.baidu.com"
    my_list=[1,2,3,4,5]
    my_dict={'name':'schrodingho','url':'www.baidu.com'}
    #模板引擎jinja2相当于由后端向前端网页中传入数据，将变量传入templates中的模板
    #render_template进行模板渲染

    #
    return render_template('1.html',url_str=url_str,my_list=my_list,my_dict=my_dict)

#变量代码块的使用

if __name__ == '__main__':
    app.run(debug=True)
