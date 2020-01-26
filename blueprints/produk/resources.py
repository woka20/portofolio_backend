from flask import Blueprint
from flask_restful import reqparse, Api, Resource,marshal
from blueprints import db,internal_required
from sqlalchemy import func
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_claims, get_jwt_identity
from ..produk.model import Products

bp_produk=Blueprint("produk", __name__)
api=Api(bp_produk)

class ProductResource(Resource):
    def __init__(self):
        pass

    
    #Admin POST product details by ID, every product posted by Admin will be have type "Premium" automatically
    @jwt_required
    @internal_required
    def post(self, id):
        parser=reqparse.RequestParser()
        parser.add_argument('tipe', location="json", default="Premium")
        parser.add_argument('user_id', type=int,location="json")
        parser.add_argument('nama_produk', location="json", required=True)
        parser.add_argument('category',location="json")
        parser.add_argument('harga', type=int,location="json")
        parser.add_argument('stok', type=int,location="json")
        parser.add_argument('berat', type=int,location="json")
        parser.add_argument('gambar', location="json")
        parser.add_argument('preview_1', location="json")
        parser.add_argument('preview_2', location="json")
        parser.add_argument('preview_3',location="json")
        parser.add_argument('description', location="json")
        args=parser.parse_args()
        
        qry=Products.query.filter_by(nama_produk=args['nama_produk']).first()
        
        #Store to Database
        if qry is None:
            produk=Products(args['tipe'],args['user_id'],args['nama_produk'], args['category'], args['harga'], args['stok'],args['berat'],args['gambar'],args['preview_1'], args['preview_2'], args['preview_3'], args['description'])
                    
            db.session.add(produk)
            db.session.commit()
            return marshal(produk, Products.response_fields), 200,{'Content-Type':'application/json'}
        else:
            return {'status':'Product is already exist'}, 403

    
    #Admin UPDATE products by ID    
    @jwt_required
    @internal_required
    def put(self,id):
        parser=reqparse.RequestParser()
        parser.add_argument('nama_produk', location="json")
        parser.add_argument('category', location="json")
        parser.add_argument('harga', type=int, location="json")
        parser.add_argument('stok', type=int,location="json")
        parser.add_argument('berat', type=int,location="json")
        parser.add_argument('gambar', location="json")
        parser.add_argument('preview_1', location="json")
        parser.add_argument('preview_2', location="json")
        parser.add_argument('preview_3', location="json")
        parser.add_argument('description', location="json")
        args=parser.parse_args()
        
        qry=Products.query.get(id)
        print("KLKL", qry)
        if qry is None:
            return {'status':'NOT FOUND'}, 404
        
        #If Admin leave some field empty, the designated empty field won't be null
        if args['nama_produk'] is '':
            qry.nama_produk=qry.nama_produk
        else:
            qry.nama_produk=args['nama_produk']

        if args['category'] is '':
            qry.category=qry.category
        else:
            qry.category=args['category']
        
        if args['harga'] is 0:
            qry.harga=qry.harga
        else:
            qry.harga=args['harga']
        
        if args['stok'] is 0:
            qry.stok=qry.stok
        else:
            qry.stok=args['stok']
        
        if args['berat'] is 0:
            qry.berat=qry.berat
        else:
            qry.berat=args['berat']

        if args['gambar'] is '':
            qry.gambar=qry.gambar
        else:
            qry.gambar=args['gambar']

        if args['preview_1'] is '':
            qry.preview_1=qry.preview_1
        else:
            qry.preview_1=args['preview_1']
        
        if args['preview_2'] is '':
            qry.preview_2=qry.preview_2
        else:
            qry.preview_2=args['preview_2']
        
        if args['preview_3'] is '':
            qry.preview_3=qry.preview_3
        else:
            qry.preview_3=args['preview_3']

        if args['description'] is '':
            qry.description=qry.description
        else:
            qry.description=args['description']
        
         #Store to Database
        db.session.commit()

        return marshal(qry, Products.response_fields), 200
    
    #Admin GET products by ID   
    @jwt_required
    def get(self,id):
        
        qry=Products.query.get(id)

        if qry is None:
            return {'status':'NOT FOUND'}, 404
        
        return marshal(qry, Products.response_fields), 200
    

    #Admin DELETE products by ID   
    @jwt_required
    @internal_required
    def delete(self,id):
        qry=Products.query.get(id)

        if qry is None:
            return {'status':'NOT FOUND'}, 403

        db.session.delete(qry)
        db.session.commit()

        return {'status':'Product has been successfully deleted'}, 200

    def options(self,id):
        return {'status': 'OK'},200

class UsedResource(Resource):
    def __init__(self):
        pass
    #Client can sell his own product to by using POST. It will be automatically labelled as "Pelapak"
    @jwt_required
    def post(self, id):
        parser=reqparse.RequestParser()
        parser.add_argument('tipe', type=str, location="json", default="Pelapak")
        parser.add_argument('user_id', type=int,location="json")
        parser.add_argument('nama_produk', location="json")
        parser.add_argument('category', location='json')
        parser.add_argument('harga', type=int, location='json')
        parser.add_argument('stok', location='json')
        parser.add_argument('berat', location='json')
        parser.add_argument('gambar', location='json')
        parser.add_argument('preview_1', location='json')
        parser.add_argument('preview_2', location='json')
        parser.add_argument('preview_3', location="json")
        parser.add_argument('description', location="json")

        args=parser.parse_args()
        
        #If it Admin, user_id will be 0 or null, if client, it will store its id stored in get_jwt_claims()['id']
        qry=Products.query.filter_by(nama_produk=args['nama_produk']).first()
        try:
            if get_jwt_claims()['jabatan'] is not None:
                bekas=Product(args['tipe'],args['user_id'],args['nama_produk'], args['category'], args['harga'], args['stok'],
                args['berat'],args['gambar'],args['preview_1'], args['preview_2'], args['preview_3'], args['description'])

        except:
            bekas=Products(args['tipe'],get_jwt_claims()['id'],args['nama_produk'], args['category'], args['harga'], args['stok'],
            args['berat'],args['gambar'],args['preview_1'], args['preview_2'], args['preview_3'], args['description'])
      
       #Store to Database
        if qry is None:
            db.session.add(bekas)
            db.session.commit()
            return {'status': "Successfully Added New Product"}, 200, {'Content-Type':'application/json'}
        else:
            return {'status':'Product is already exist'}, 403
    
    #Clients UPDATE Detail of the product their posted only, other product from other user cannot be accesed by them. 
    @jwt_required
    def put(self,id):
        parser=reqparse.RequestParser()
        parser.add_argument('nama_produk', location="json")
        parser.add_argument('category', location='json')
        parser.add_argument('harga', type=int, location='json')
        parser.add_argument('stok', type=int, location='json')
        parser.add_argument('berat', location='json')
        parser.add_argument('gambar', location='json')
        parser.add_argument('preview_1', location='json')
        parser.add_argument('preview_2', location='json')
        parser.add_argument('preview_3', location="json")
        parser.add_argument('description', location="json")

        args=parser.parse_args()
        try:
            if get_jwt_claims()['id'] is not None:
                qry=Products.query.filter_by(user_id=get_jwt_claims()['id']).all()
               
        except:
             qry=Products.query.filter_by(id=id).all()

         #If client leave some field empty, the designated empty field won't be null
        for i in qry:
            if i.id==id:
            
                
                if args['nama_produk'] is '':
                    i.nama_produk=i.nama_produk
                else:
                    i.nama_produk=args['nama_produk']
                    
                if args['category'] is '':
                    i.category=i.category
                else:
                    i.category=args['category']
                if args['harga'] is 0:
                    i.harga=i.harga
                else:
                    i.harga=args['harga']
        
                if args['stok'] is 0:
                    i.stok=i.stok
                else:
                    i.stok=args['stok']

                if args['berat'] is '':
                    i.berat=i.berat
                else:
                    i.berat=args['berat']

                if args['gambar'] is '':
                    i.gambar=i.gambar
                else:
                    i.gambar=args['gambar']
                if args['preview_1'] is '':
                    i.preview_1=i.preview_1
                else:
                    i.preview_1=args['preview_1']
                if args['preview_2'] is '':
                    i.preview_2=i.preview_2
                else:
                    i.preview_2=args['preview_2']
                if args['preview_3'] is '':
                    i.preview_3=i.preview_3
                else:
                    i.preview_3=args['preview_3']
                    
                if args['description'] is '':
                    i.description=i.description
                else:
                    i.description_1=args['description']

                #Store to database
                db.session.commit()
                return marshal(i, Products.response_fields), 200
            else:
                return {'status':'NOT FOUND'}, 403

        
    #Client (even without login) GET product detail by ID if they want to buy something here
    def get(self, id):
        qry=Products.query.get(id)

        if qry is None:
            return {'status':'NOT FOUND'}, 403

        return marshal(qry, Products.response_fields), 200

    #Client DELETE of the product their posted only, other product from other user cannot be accesed by them.
    @jwt_required
    def delete(self,id):
        qry=Products.query.filter_by(user_id=get_jwt_claims()['id']).all()
        
        for i in qry:
            if i.id==id:
                qry_new=i
            else:
                qry_new=''

        if qry_new is None:
            return {'status':'NOT FOUND'}, 403
        
        db.session.delete(qry_new)
        db.session.commit()

        return {'status':"Delete Success"},200

    def options(self,id):
        return {'status': 'OK'},200
    
   
class ProductList(Resource):
    #All can GET list of available products in this e-commerce website
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('p', location='args', type=int,default=1)  
        parser.add_argument('rp', location='args', type=int, default=25)
        args=parser.parse_args()

        qry=Products.query

        offset=(args['p']*args['rp'])-args['rp']

        #looping all quaery to provide list of products
        rows=[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Products.response_fields))
        return rows, 200

    def options(self):
        return {'status': 'OK'},200


#ENDPOINTS
api.add_resource(ProductResource, '','/premium/<int:id>')
api.add_resource(UsedResource, '','/used/<int:id>')
api.add_resource(ProductList,'','/list')