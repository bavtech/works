from datetime import datetime

from flaskInterface import db  ,login_manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    
    return  User.query.get(int(user_id))


class TaskView(ModelView):

    column_display_pk=True
    column_hide_backrefs = False
    column_list = ('id','title', 'domain', 'date_created','created_by')

class DomainView(ModelView):

    column_display_pk=True
    column_hide_backrefs = False
    column_list = ('title', 'description','created_by')

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email =  db.Column(db.String(100),unique=True,nullable=False)
    password =  db.Column(db.String(60), nullable=False)


    def __str__(self):
        return f"User-{self.username} "


class Domain(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32),nullable=False)
    description =  db.Column(db.Text, nullable=False)

    created_by =  db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)


    def __str__(self):
        return self.title

class Task(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(62),nullable=False)
    domain  =  db.Column(db.String, db.ForeignKey('domain.title'), nullable=False)
    date_created =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by =  db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    # data_file =  db.Column(db.String(120), nullable=False)

    def __str__(self):
        return f'Task:-->{self.title} ----- Domain:--> {self.domain}'

