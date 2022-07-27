from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField , BooleanField, SelectField
from wtforms.validators import DataRequired,EqualTo,Length,Email ,ValidationError
from flaskInterface.models import User,Domain,Task 
from flask_login import  current_user
from flask_wtf.file  import FileField, FileAllowed

# # from models import  Domain,Task




def object_reveal(model):
    container = []
    for i in model.query.all() :
        container.append((i,i))

    return container



class  RegistrationForm(FlaskForm):

    username =  StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])

    email =  StringField('Email', validators=[DataRequired(),Email()])
    password  =PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(),EqualTo('password')]) 

    submit = SubmitField('Sign Up')


        

class  LoginForm (FlaskForm):

   
    email =  StringField('Email', validators=[DataRequired(),Email()])
    password  =PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember me')

    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    
    
    task_name =  StringField('Task Name', validators=[DataRequired()])
    desired_output =  SelectField(u'Export Type',choices=[('CSV','CSV'),('Excel','XLSX')] )
    taskDomain = SelectField(u'Domains', choices=object_reveal(Domain) )
    fileInput =  FileField(u'Preferably CSV', validators=[FileAllowed(['csv','xlsx'])])
    gpu = BooleanField()
    submit =  SubmitField('Start')
     
class DomainForm(FlaskForm):

    title = StringField('Domain Name', validators=[DataRequired()])
    description= StringField("Description", validators=[DataRequired()])
    created_by =  StringField('Domain Author', validators=[DataRequired()],default=current_user.username if current_user else 'Anonymous')
    submit  = SubmitField("Create")




