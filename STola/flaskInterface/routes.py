
from flask import  render_template,flash, redirect, url_for
from flaskInterface.forms import RegistrationForm, LoginForm, TaskForm,DomainForm
from flaskInterface.models  import Domain, Task, User,ModelView, TaskView, DomainView
from flaskInterface import app,db, bcrypt
from flask_admin import Admin 
from flask_login import login_user, current_user, logout_user,login_required
import pandas  as pd 
import os, secrets 

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(TaskView(Task, db.session))
admin.add_view(DomainView(Domain, db.session))

def saveUploads(Fname):
    random_hex = secrets.token_hex(8)
    print(Fname)
    _, f_ext = os.path.splitext(Fname)
    file_rn =  random_hex + f_ext
    print(file_rn)
    file_path  = os.path.join(app.root_path,'static/datas', '{file_rn}')

    return file_path

@app.route('/')
@app.route('/home')
def Home():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def Login():

    if current_user.is_authenticated:
        return  redirect(url_for('Home'))
    form =LoginForm()
    

    if form.validate_on_submit():
        
        user =  User.query.filter_by(email=form.email.data).first()
        

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data )
            print(bcrypt.generate_password_hash(form.password.data))

            print("new password")
            print(user.password)
            return redirect(url_for('Home'))

        else:
            flash('Login unsuccessful. please  check username and password')
    return render_template('login.html',title='Login', form=form)


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return  redirect(url_for('Home'))
    form =  RegistrationForm()

    if form.validate_on_submit():
        hashed_password =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user =  User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created you can   now login', 'bg-red-100')
        return redirect(url_for('Login'))

    return render_template('register.html',title='Register', form=form)


@app.route('/job/task', methods=['GET','POST'])
@login_required
def Job():
    form =  TaskForm()
    if form.validate_on_submit():
        # upFile =  saveUploads(form.fileInput.data)
        task  = Task(title=form.task_name.data, domain=form.taskDomain.data, created_by=current_user.username)
       
        db.session.add(task)
        db.session.commit()
        

        Dataframe =  pd.read_csv(form.fileInput.data)
        print(Dataframe.head())

    return render_template('create_job.html',title='jobs', form=form)
    
@app.route('/job/task/addDomain',methods=['GET','POST'])
@login_required
def Dom():
    form =  DomainForm()
    if form.validate_on_submit():
        domain =  Domain(title=form.title.data, description=form.description.data, created_by=current_user.username)
        db.session.add(domain)
        db.session.commit()
        flash(f'New Domain Added')
        


    return render_template('addDomain.html',title='jobs', form=form)

@app.route('/logout', methods=['GET','POST'])
def logout():

    logout_user()

    return redirect(url_for('Home'))