from flask import Blueprint,request, render_template,Flask
from flask_restful import reqparse, Api, Resource,marshal
from blueprints import db,internal_required
from sqlalchemy import func
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_claims, get_jwt_identity
from ..belanja.model import Shoppings
from ..produk.model import Products
from ..konsumen.model import Costumers
import requests
import json
from json.encoder import JSONEncoder
from PIL import Image
import io
from io import BytesIO
import base64
##
bp_belanja=Blueprint("belanja", __name__)
api=Api(bp_belanja)

ongkir_host="https://api.rajaongkir.com/starter"
ongkir_key="fb63156a683784f4edbd8f23ea73a4a3"

#Function to access Third Party API Rajaongkir, to check Cost of Delivery
def post_rajaongkir(host,pengirim,penerima, berat, kurir, key):
    rq=requests.post(host+'/cost', data={'origin': pengirim, 'destination': penerima,
        'weight': berat,'courier':kurir,'key': key})
    b=rq.json()
    return b

class Cart(Resource):
    def __init__(self):
        pass
    
    #POST Function To Add Shopping Cart (Accessed by Client)
    @jwt_required
    def post(self):
        id_1= get_jwt_claims()['id']

        parser=reqparse.RequestParser()
        parser.add_argument('user_id',location='args', type=int)
        parser.add_argument('product_id', location='args', type=int)
        parser.add_argument('kurir', location='args')
        parser.add_argument('quantity',type=int, location='args')
        parser.add_argument('ongkir', location='args', type=int)
        parser.add_argument('total_harga',location='args')
        parser.add_argument('payment', location="args", default="Belum Bayar")
        parser.add_argument('bukti_pembayaran', default=None, location="args")
        
        args=parser.parse_args()
        
        #Find product data, based on its 'product_id'
        qry_product=Products.query.get(args['product_id'])
        qry_user=Costumers.query.get(qry_product.user_id)
        qry_order=Shoppings.query.filter_by(id=id_1).filter_by(payment="Belum Bayar").first()
        print("PPPPPPPPPPP", qry_order)
        #API RajaOngkir cannot process order with total weight more than 30 Kg. (Input must be in gram)
        if (args['quantity']*qry_product.berat)> 30000:
            return {'message': "Berat total pesanan Anda harus di bawah 30 Kg"}, 403
        
        #If type of query is "Premium", origin city is Malang(256) as headquarter of this e-commerce in order
        #to calculate Delivery fee(ongkir)
        if qry_product.tipe == "Premium":
            biaya=post_rajaongkir(ongkir_host, 256, get_jwt_claims()['kota'],args['quantity']*qry_product.berat,args['kurir'],ongkir_key)
            
        else:
            #else, origin city based on city of the seller address using "qry_user.kota"
            biaya=post_rajaongkir(ongkir_host, qry_user.kota, get_jwt_claims()['kota'],args['quantity']*qry_product.berat,args['kurir'],ongkir_key )
            
        #Find its Delivery Fee from JSON result generated by "post_rajaongkir" function
        hasil=biaya['rajaongkir']['results']
        list_harga=hasil[0]['costs']
        daftar_harga=[]

        #Append all the delivery services option input from ["jne", "pos","tiki"]
        for opsi in list_harga:
           for j in opsi['cost']:
               daftar_harga.append({opsi['service']:j['value']})
        
        #For now, I provide with"REG" delivery type from all providers
        for paket in daftar_harga:
            try:
                if paket['REG'] is not None:
                    ongkir=paket['REG']
            except:
                continue
        #If the client order quantity more than available stock, it cannot be processed
        if args['quantity']>qry_product.stok:
            return {'status': 'Your order quantity is exceeding the available stocks' }, 403
            
        elif qry_order is not None:
            return {'status':"You haven't paid another order, paid it first to make new order"}, 403
 
            
        else:
            shop=Shoppings(id_1, args['product_id'], args['quantity'], args['kurir'], ongkir, 
                          ongkir+(args['quantity']*qry_product.harga), args['payment'], args['bukti_pembayaran'])
          
            db.session.add(shop)
            db.session.commit()

            return marshal(shop, Shoppings.response_fields),200
    
    #GET Function To see Shopping Cart's detail (Accessed by Client)
    @jwt_required
    def get(self):
        id_1=get_jwt_claims()['id']
        
        #Creating dictionary by retrieve ordered product's detail from Products's Database and insert to shopping detail
        qry=Shoppings.query.filter_by(id=id_1).first()
        daftar=[]
        print("OOOOOOOOOOO",id_1)
        marshalCart=marshal(qry, Shoppings.response_fields)
        qry_produk=Products.query.get(marshalCart["product_id"])
        marshalProduct=marshal(qry_produk, Products.response_fields)
        marshalCart['Product']=marshalProduct

        
        #Creating dictionary by retrieve ordered buyer's detail in Customer's database and insert to shopping detail
        qry_user=Costumers.query.get(get_jwt_claims()['id'])
        marshalUser=marshal(qry_user, Costumers.response_fields)
        marshalCart["Buyer"]=marshalUser
        
     
        if qry is not None:
          
            return marshalCart,200
        else:
          
            return {'status':'NOT FOUND'}, 404

    def options(self):
        return {'status': 'OK'},200


class Checkout(Resource):
    #GET Function To see Shopping Checkout's detail (Accessed by Client) list
     @jwt_required
     def get(self):

        parser=reqparse.RequestParser()
        parser.add_argument('rp',location='args', type=int,default=25)
        parser.add_argument('p', location='args', type=int, default=1)
        args=parser.parse_args()

        qry=Shoppings.query.filter_by(user_id=get_jwt_claims()['id'])
    
        if qry is None:
              return {'status':'NOT FOUND'}, 403

        offset=(args['rp']*args['p'])-args['rp']
        
        #generate the list of order by this client
        rows=[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Shoppings.response_fields))
            
        return rows, 200
     
     #UPDATE Function To Shopping Checkout's detail (Accessed by Admin, to update payment status of particular buyer) 
     @internal_required
     @jwt_required 
     def put(self):

        parser=reqparse.RequestParser()
        parser.add_argument('id',location='json') 
        parser.add_argument('user_id',location='json')
        parser.add_argument('product_id', location='json', type=int)
        parser.add_argument('quantity',location='json')
        parser.add_argument('ongkir', location='json', type=int)
        parser.add_argument('total_harga',location='json')
        parser.add_argument('payment',location="json")
        parser.add_argument('bukti_pembayaran', location="json")
        
        args=parser.parse_args()
        
        qry=Shoppings.query.get(args['id'])
        if qry is None:
            return {'status':'NOT FOUND'}, 404
        
        #if there is no input while update, it won be a null in database
        if args['payment'] is None:
            qry.payment=qry.payment
        else:
            qry.payment=args['payment']   

        return marshal(qry, Shoppings.response_fields), 200

     def options(self):
        return {'status': 'OK'},200
            


class Confirmation(Resource):
    ##UPDATE Function Shopping Checkout's detail (Accessed by Client) to add image of Transfer Receipt
    @jwt_required
    def put(self, id):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',location='args')
        parser.add_argument('product_id', location='json',type=int)
        parser.add_argument('quantity',location='json')
        parser.add_argument('ongkir', location='json', type=int)
        parser.add_argument('total_harga',location='json')
        parser.add_argument('payment',location="json")
        parser.add_argument('bukti_pembayaran', location="json")
        
        args=parser.parse_args()

        qry=Shoppings.query.filter_by(user_id=get_jwt_claims()['id']).all()
        
        #Uploaded transfer receipt in img format will be converted in to Hexbinary by using getvalue()
        #args['bukti Pembayaran'] is the image name and path to be uploaded
        file_bukti=Image.open(BytesIO(base64.b64decode(args['bukti_pembayaran'])))
        output=io.BytesIO()
        file_bukti.save(output, format="JPEG")
        hex_data=output.getvalue()
        

        #Hex will be stored in database as a BLOB, so it can be decode to image again to be verified by admin regarding 
        #client payment status
        for i in qry:
            if i.id==id:
                if args['bukti_pembayaran'] is None:
                    i.bukti_pembayaran=i.bukti_pembayaran
                else:
                    i.bukti_pembayaran=hex_data
            else:
              return {'status':'NOT FOUND'}, 404
        
        #commit to dtaabase
        db.session.commit()
        

        return {'status':"Bukti Pembayaran Berhasil Disubmit. Tunggu verifikasi dari kami"}, 200


    def options(self, id):
        return {'status': 'OK'},200


#ENDPOINTS
api.add_resource(Cart, '','/cart')
api.add_resource(Checkout,'','/checkout')
api.add_resource(Confirmation,'','/confirm/<int:id>')
