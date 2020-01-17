from blueprints import db
import datetime
from flask_restful import fields

class Products(db.Model):
    __tablename__="produk"
    id=db.Column (db.Integer, primary_key=True, autoincrement=True)
    tipe=db.Column(db.String(10),nullable=True)
    user_id= db.Column (db.Integer, nullable=True)
    nama_produk=db.Column (db.String(100))
    category=db.Column (db.String(100))
    harga=db.Column (db.Integer, nullable=True)
    stok=db.Column (db.Integer, nullable=True)
    berat=db.Column (db.Integer, nullable=True)
    gambar=db.Column (db.String(200), nullable=True)
    preview_1=db.Column (db.String(200), nullable=True)
    preview_2=db.Column (db.String(200), nullable=True)
    preview_3=db.Column (db.String(200), nullable=True)
    description= db.Column (db.String(1000))
    created_at=db.Column (db.DateTime, default=datetime.datetime.now)
    updated_at=db.Column (db.DateTime, onupdate=datetime.datetime.now)
    deleted_at=db.Column (db.Boolean, default=None)
    
    response_fields={
        'id':fields.Integer,
        'tipe':fields.String,
        'user_id':fields.Integer,
        'nama_produk':fields.String,
        'category':fields.String,
        'harga':fields.Integer,
        'stok':fields.Integer,
        'berat':fields.Integer,
        'gambar':fields.String,
        'preview_1':fields.String,
        'preview_2':fields.String,
        'preview_3':fields.String,
        'description': fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        'deleted_at':fields.Boolean
    }
    
    def __init__(self,tipe,user_id,produk, kategori, harga, stok,berat,gambar,preview1,preview2,preview3, deskripsi):
        self.tipe=tipe
        self.user_id=user_id
        self.nama_produk=produk
        self.category=kategori
        self.harga=harga
        self.stok=stok
        self.berat=berat
        self.gambar=gambar
        self.preview_1=preview1
        self.preview_2=preview2
        self.preview_3=preview3
        self.description=deskripsi
        
    def __repr__ (self):
        return "<produk %r>" %self.id
