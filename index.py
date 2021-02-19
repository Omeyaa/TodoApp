from flask import Flask, render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
#config app
app.config['SECRET_KEY'] = 'Omeyaa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#set database to app
db = SQLAlchemy(app)
Bootstrap(app)

#create table 1 
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    date_now = db.Column(db.String(64),nullable=False,unique=True)
    date = db.Column(db.String(64),nullable=False,unique=True)
    days = db.relationship('Day',backref='todos',lazy=True)
    
#create table 2
class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(64),unique = True,nullable=False)
    remark = db.Column(db.String(200),nullable=False)
    time = db.Column(db.String(64),nullable=False)
    todo_id = db.Column(db.Integer,db.ForeignKey('todos.id'),nullable=False)
    
#create form
class Form(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    date = StringField("Date",validators=[DataRequired()])
    remark = TextAreaField('Remark',validators=[DataRequired()])
    time = StringField('Time',validators=[DataRequired()])
    submit= SubmitField("Create",validators=[DataRequired()])
    btn_del = SubmitField("Remove",validators=[DataRequired()])

#homepage
@app.route('/')
def home():
    return render_template('home.html')

#index page
@app.route('/Todo',methods = ['GET','POST'])
def index():
    form = Form()
    if request.method == "POST":
        datetime_for_string = datetime.now()
        datetime_string_format = '%b %d %Y, %H:%M:%S'
        now = datetime.strftime( datetime_for_string, datetime_string_format)
        date1 = form.date.data
        db.session.add(Todo(date=date1,date_now = now))
        db.session.commit()
        flash('Successully Added')
        return redirect('/Todo')
    return render_template('index.html',form = form,todo=Todo.query.all())

#delete 
@app.route('/delete/<int:_id>')
def delete(_id):
    del_row = Todo.query.filter_by(id=_id).first()
    day = Day.query.filter_by(todo_id = _id).first()
    db.session.delete(del_row)
    if day is not None:
        db.session.delete(day)
    db.session.commit()
    return redirect('/Todo')

#view
@app.route('/view/<date>/<id>',methods=['POST','GET'])
def view(date,id):
    form = Form()
    if request.method == 'POST':
        todo_by_id = Todo.query.filter_by(id=id).first()
        todo_db = Todo(date_now = todo_by_id.date_now,date= todo_by_id.date)
        title = form.title.data
        remark = form.remark.data
        time = form.time.data
        child = Day(title=title,remark=remark,time=time,todos= todo_by_id)
        db.session.add(child)
        db.session.commit()
        return redirect(f'/view/{date}/{id}')
    return render_template('list.html',form=form,list = Day.query.filter_by(todo_id=id).all() ,date = date)

#delete
@app.route('/Delete/<date>/<id>')
def delete_row(id,date):
    del_row = Day.query.filter_by(id=id).first()
    db.session.delete(del_row)
    db.session.commit()
    return redirect((f'/view/{date}/{id}'))


if __name__ == '__main__':
  app.run()
    

