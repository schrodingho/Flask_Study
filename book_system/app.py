from flask import Flask,render_template,flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key='123hdsufsdui31urewf'
#数据库配置
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1/flask_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者:',validators=[DataRequired()])
    book = StringField('书籍:',validators=[DataRequired()])
    submit = SubmitField('提交')

#创建数据库
db=SQLAlchemy(app)

class Author(db.Model):
    __tablename__='authors'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(16),unique=True)
    #books是给自己（Author）用的，author是给Book模型用的
    books=db.relationship('Book',backref='author')#relationship这用模型名

    def __repr__(self):
        return '<Author: %s %s >' % (self.id, self.name)



class Book(db.Model):
    __tablename__='books'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=True)

    #外键对,在Book模型中建立author_id，与authors表中的id关联
    author_id=db.Column(db.Integer, db.ForeignKey('authors.id'))#foreignkey这里用表名

    def __repr__(self):
        return '<Book: %s %s >' % (self.id, self.name)


# 删除表
db.drop_all()
# 创建表
db.create_all()

au1=Author(name='鲁迅')
au2=Author(name='胡适')

db.session.add_all([au1,au2])
db.session.commit()

bk1=Book(name='朝花夕拾',author_id=au1.id)
bk2=Book(name='狂人日记',author_id=au1.id)
bk3=Book(name='野草集',author_id=au1.id)
bk4=Book(name='白话文学史',author_id=au2.id)
bk5=Book(name='说儒',author_id=au2.id)
bk6=Book(name='尝试集',author_id=au2.id)

db.session.add_all([bk1,bk2,bk3,bk4,bk5,bk6])
db.session.commit()

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    #查询数据库，查询是否有该id的书，有就删，没有就error
    book=Book.query.get(book_id)

    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除书籍出错')
            db.session.rollback()

    else:
        flash('书籍找不到')

    #返回当前网址--》重定向,需要传入一个网址
    return redirect(url_for('index'))#url_for('index')传入视图函数名，返回视图函数对应地址


@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    #先删书，再删作者
    author=Author.query.get(author_id)

    if author:
        try:
            #查询后直接删除
            Book.query.filter_by(author_id=author.id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除作者出错')
            db.session.rollback()
    else:
        flash("作者找不到")

    return redirect(url_for('index'))


@app.route('/',methods=['GET','POST'])
def index():
    #创建自定义表单类
    author_form=AuthorForm()
    #验证逻辑：调用wtf实现验证
    #验证通过获取数据
    #判断作者是否存在
    #如果作者存在，再来判断书籍是否存在，没有重复添加书籍，重复error
    #如果作者不存在，添加作者和书籍
    #如果验证不通过，错误
    if author_form.validate_on_submit():
        #获取表单数据
        author_name=author_form.author.data
        book_name=author_form.book.data
        #数据库查询
        author=Author.query.filter_by(name=author_name).first()

        if author:
            #判断书籍是否存在，没有重复添加书籍，重复error
            book=Book.query.filter_by(name=book_name).first()

            if book:
                flash('已存在同名书籍')
            else:
                try:
                    new_book=Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加书籍失败')
                    db.session.rollback()#回滚
        else:#加入数据
            try:
                new_author=Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book=Book(name=book_name,author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash('添加新的作者和书籍失败')
                db.session.rollback()

    else:
        if request.method=='POST':
            flash('参数不全')

    #查询作者信息
    authors=Author.query.all()

    return render_template('books.html',authors=authors,form=author_form)



if __name__ == '__main__':
    app.run()
