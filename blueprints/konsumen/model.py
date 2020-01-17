from blueprints import db
from flask_restful import fields
import datetime

class Costumers(db.Model):
    __tablename__="konsumen"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    client_name=db.Column(db.String(100), nullable=True)
    client_password=db.Column(db.String(1000), nullable=True)
    full_name=db.Column(db.String(100), nullable=True)
    telp=db.Column(db.String(13),nullable=True)
    email=db.Column(db.VARCHAR(100),nullable=True)
    kota=db.Column(db.String(100), nullable=True)
    created_at=db.Column (db.DateTime, default=datetime.datetime.now)
    updated_at=db.Column (db.DateTime, onupdate=datetime.datetime.now)
    deleted_at=db.Column (db.Boolean, default=None)

    response_fields={
        'id':fields.Integer,
        'client_name':fields.String,
        'client_password':fields.String,
        'full_name':fields.String,
        'telp':fields.String,
        'email':fields.String,
        'kota':fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        'deleted_at':fields.Boolean,
    }

    jwt_claims_fields={
        'id':fields.Integer,
        'client_name':fields.String,
        'client_password':fields.String,
        'full_name':fields.String,
        'telp':fields.Integer,
        'email':fields.String,
        'kota':fields.String,

    }

    def __init__(self, username,password,nama,telp,email,kota ):
        self.client_name=username
        self.client_password=password
        self.full_name=nama
        self.telp=telp
        self.email=email
        self.kota=kota

    def __repr__(self):
        return "<konsumen %r>" %self.id