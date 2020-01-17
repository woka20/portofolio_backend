from blueprints import db
import datetime
from flask_restful import fields

class Shoppings(db.Model):
    __tablename__="belanja"
    id=db.Column (db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('konsumen.id'), nullable=True)
    product_id=db.Column (db.Integer, db.ForeignKey('produk.id'),nullable=True)
    quantity=db.Column(db.Integer,nullable=True)
    kurir=db.Column(db.String(10),nullable=True)
    ongkir=db.Column(db.Integer, nullable=True)
    total_harga=db.Column(db.Integer, nullable=True)
    payment=db.Column(db.String(20), nullable=True)
    bukti_pembayaran=db.Column(db.LargeBinary, nullable=True)
    created_at=db.Column (db.DateTime, default=datetime.datetime.now)
    updated_at=db.Column (db.DateTime, onupdate=datetime.datetime.now)
    deleted_at=db.Column (db.Boolean, default=None)
    
    response_fields={
        'id':fields.Integer,
        'user_id':fields.Integer,
        'product_id':fields.Integer,
        'quantity':fields.Integer,
        'kurir':fields.String,
        'ongkir':fields.Integer,
        'total_harga':fields.Integer,
        'payment':fields.String,
        'bukti_pembayaran': fields.String,
        'created_at':fields.DateTime,
        'updated_at':fields.DateTime,
        'deleted_at':fields.Boolean
    }
    
    def __init__(self,user_id,product_id,quantity,kurir,ongkir,total_harga,payment, binary):
        self.user_id=user_id
        self.product_id=product_id
        self.quantity=quantity
        self.kurir=kurir
        self.ongkir=ongkir
        self.total_harga=total_harga
        self.payment=payment
        self.bukti_pembayaran=binary
        
        
    def __repr__ (self):
        return "<belanja %r>" %self.id
