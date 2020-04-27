from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import uuid
from application import app
db = SQLAlchemy(app)
import datetime
class Versemment(db.Model):
    __tablename__="versement"
    id=db.Column(UUID(as_uuid=True),primary_key=True,default=db.text("uuid_generate_v4()"))
    date=db.Column(db.DateTime)
    UsdPrice=db.Column(db.Float, nullable=False)
    MroAmount=db.Column(db.Float, nullable=False)

    def __repr__():
        return "date:{date},Amount:{mro}".format(date=self.date,mro=self.MroAmount)

class Client(db.Model):
    __tablename__="client"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=db.text("uuid_generate_v4()" ))
    fullname=db.Column(db.String, nullable=False)
    socialAdress=db.Column(db.String,nullable=True)
    socialType=db.Column(db.String,nullable=True)
    Description=db.Column(db.Text,nullable=True)
    
    def __repr__():
        return "Full Name:{name} phone Number:{phone}".format(name=self.name,phone=self.phone)

class Transaction(db.Model):
    __tablename__="transaction"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=db.text("uuid_generate_v4()"))
    boughtProduct=db.Column(UUID(as_uuid=True),db.ForeignKey("product.id"),nullable=False)
    Client=db.Column(UUID(as_uuid=True),db.ForeignKey("client.id"),nullable=True)
    Description=db.Column(db.Text,nullable=True)
    Date= db.column(db.DateTime)

    TransactionId=db.Column(db.Text,nullable=True)
    product= db.relationship("Product", backref="Transaction", lazy=True)
    
class Product(db.Model):
    __tablename__="product"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=db.text("uuid_generate_v4()"))
    name= db.Column(db.String,nullable=False)
    UsdPrice=db.Column(db.Float, nullable=False)
    MroPrice=db.Column(db.Float, nullable=False)
    MroSellPrice=db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return self.name

class User(db.Model,UserMixin):
    __tablename__='user'
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    def get_id(self):
        return self.username


class Total(db.Model,UserMixin):
    __tablename__="total"
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=db.text("uuid_generate_v4()"))
    montant= db.Column(db.String,nullable=False)
    Date= db.column(db.DateTime)
    
    