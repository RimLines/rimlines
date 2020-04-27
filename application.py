from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user
from flask_hashing import Hashing
import os
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView

#from Models import db


class myModelView(ModelView):
    def is_accessible(self):
        if current_user==None:
            return False
        return current_user.is_authenticated
    def inaccessible_callback(self):
        return redirect(url_for('login'))

class myAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user==None:
            return False
        return current_user.is_authenticated
    def inaccessible_callback(self):
        return redirect(url_for('login'))



app=Flask(__name__)
from Models import *
admin = Admin(app,index_view=myAdminIndexView())

login=LoginManager(app)
hashing = Hashing(app)

from flask_admin.contrib.sqla import ModelView

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.config['SQLALCHEMY_DATABASE_URI']="postgres://dxwmauetirkoiw:651a9e88220600d6efa363350d0ad7913568ed265f9065d7ac23eee5496ca4a3@ec2-54-247-96-169.eu-west-1.compute.amazonaws.com:5432/d57bjg6fkpv8l3"
app.config['SECRET_KEY']="DBDDRFLsg21brgh45FFg43vol"

admin.add_view(myModelView(Versemment,db.session))
admin.add_view(myModelView(Client,db.session))
admin.add_view(myModelView(Product,db.session))
admin.add_view(myModelView(Transaction,db.session))
admin.add_view(myModelView(User,db.session))

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']

        if username==None or password==None:
            return render_template("login.html")

        user=User.query.get(username.lower())
        if user==None:
            return render_template("login.html")
        if hashing.check_value(user.password, password,salt= os.getenv("HASH_KEY")):
            login_user(user)
            return redirect('/admin')

        else:
            return render_template("login.html")

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return render_template("login.html")



if __name__=='__main__':
    app.run(Debug=True)
