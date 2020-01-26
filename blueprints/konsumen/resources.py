from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from .model import Costumers
from sqlalchemy import *
from blueprints import db
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from password_strength import PasswordPolicy
import hashlib
from .model import Costumers
import requests

bp_costumer=Blueprint('konsumen', __name__)
api=Api(bp_costumer, catch_all_404s=True)

ongkir_host="https://api.rajaongkir.com/starter"
ongkir_key="fb63156a683784f4edbd8f23ea73a4a3"

#Function to access Third Party API Rajaongkir, to GET id of city name
#p is host URL and q is the API KEY
def get_rajaongkir(p,q):
    rq=requests.get(p+'/city', params={'key':q})
    b=rq.json()
    return b

class ClientResource(Resource):

    def __init__(self):
        pass

    def options(self,id):
        return {'status': 'OK'},200
    
    #Function to UPDATE client detail by Non-Admin
    @jwt_required
    def put(self, id):
        if id == get_jwt_claims()['id']:
            qry=Costumers.query.get(id)
            parser=reqparse.RequestParser()
            parser.add_argument('client_name', location="json")
            parser.add_argument('client_password', location="json")
            parser.add_argument('full_name', location="json")
            parser.add_argument('telp', location="json")
            parser.add_argument('email',location="json")
            parser.add_argument('kota', location="json")

            args=parser.parse_args()
            

            biaya=get_rajaongkir(ongkir_host, ongkir_key)
            

            
            if qry is None:
                return {'status':'NOT FOUND'}, 404

            #If client leave some field empty, the designated empty field won't be null
            if args['client_name'] is None:
                qry.client_name=qry.client_name
            else:
                qry.client_name=args['client_name']
            if args['client_password'] is None:
                qry.client_password=qry.client_password
            else:
                qry.client_password=hashlib.md5(args['client_password'].encode()).hexdigest()
            
            if args['full_name'] is '':
                qry.full_name=qry.full_name
            else:
                qry.full_name=args['full_name']
        
            if args['telp'] is '':
                qry.telp=qry.telp
            else:
                qry.telp=args['telp']
            
            if args['email'] is None:
                qry.email=qry.email
            else:
                qry.email=args['email']
            
            if args['kota'] is '':
                qry.kota=qry.kota
            else:
                #find city id from city name entered by cient
                #API RajaOngkir only can process city id not city name
                for i in biaya['rajaongkir']['results']:
                    if i['city_name'].lower()==args['kota'].lower():
                        id_kota=i['city_id']
                        qry.kota=id_kota
                
            db.session.commit()
            
            return marshal(qry, Costumers.response_fields), 200
        else:
            return {'status':'You cannot access other costumer data'},403

    #Function to Get client detail by ID, both Admin and Non-admin can access this
    @jwt_required
    def get(self,id):
        #using id stored in jwt_claims
        if id == get_jwt_claims()['id']:
            qry=Costumers.query.get(id)
            
            if qry is not None:
                return marshal(qry, Costumers.response_fields),200
            else:
                return {'status':'NOT FOUND'}, 404
        else:
            return {'status':'You cannot access other costumer data'},403

class ClientAdmin(Resource):

    def __init__(self):
        pass
    #Admin POST new client data to dtabase
    @jwt_required
    @internal_required
    def post(self,id):
        parser=reqparse.RequestParser()
        parser.add_argument('client_name', type=str, location="json")
        parser.add_argument('client_password', type=str,location="json")
        parser.add_argument('full_name', type=str,location="json")
        parser.add_argument('telp', type=str,location="json")
        parser.add_argument('email',location="json")
        parser.add_argument('kota',type=str, location="json")

        args=parser.parse_args()

        #In order to avoiding same username and email address entered more than one in db, we sshould define the condition
        qry_username=Costumers.query.filter_by(client_name=args['client_name']).first()
        qry_email=Costumers.query.filter_by(email=args['email']).first()
        result_username=marshal(qry_username, Costumers.response_fields)
        result_email=marshal(qry_email, Costumers.response_fields)
        
        if result_username['client_name'] != args['client_name'] and result_email['email'] != args['email']:
            hidden_password=hashlib.md5(args['client_password'].encode()).hexdigest()
            client=Costumers(args['client_name'], hidden_password, args['full_name'],args['telp'], args['email'], args['kota'])

            db.session.add(client)
            db.session.commit()

            return {'status':'New customers successfully added to database'},200
        else:
            return {'status':'Username or Email is already taken'}, 403

    # Admin make an update to client detail in database
    @jwt_required
    @internal_required
    def put(self, id):
       
        qry=Costumers.query.get(id)
        
        parser=reqparse.RequestParser()
        parser.add_argument('client_name', type=str,location="json",required=False)
        parser.add_argument('client_password', type=str, location="json",required=False)
        parser.add_argument('full_name', type=str,location="json",required=False)
        parser.add_argument('telp',location="json",required=False)
        parser.add_argument('email',location="args", required=False)
        parser.add_argument('kota', type=str, location="json",required=False)
   
        args=parser.parse_args()

        biaya=get_rajaongkir(ongkir_host, ongkir_key)

         #If Admin leave some field empty, the designated empty field won't be null
        if qry is None:
            return {'status':'NOT FOUND'}, 404

        if args['client_name'] is None:
            qry.client_name=qry.client_name
        else:
            qry.client_name=args['client_name']
        
        if args['client_password'] is None:
            qry.client_password=qry.client_password
        else:
            qry.client_password=hashlib.md5(args['client_password'].encode()).hexdigest()
        
        if args['full_name'] is None:
            qry.full_name=qry.full_name
        else:
            qry.full_name=args['full_name']
        
        if args['telp'] is "":
            qry.telp=qry.telp
        else:
            qry.telp=args['telp']

        if args['email'] is None:
            qry.email=qry.email
        else:
            qry.email=args['email']

        if args['kota'] is None:
            qry.kota=qry.kota
        else:
            #find city id from city name entered by cient
            #API RajaOngkir only can process city id not city name
            for i in biaya['rajaongkir']['results']:
                if i['city_name'].lower()==args['kota'].lower():
                    id_kota=i['city_id']
            qry.kota=id_kota


        db.session.commit()

        return marshal(qry, Costumers.response_fields), 200
    
    #Admin GET client details by ID
    @jwt_required
    @internal_required
    def get(self,id):
        
        qry=Costumers.query.get(id)
            
        if qry is not None:
            return marshal(qry, Costumers.response_fields),200
        else:
            return {'status':'NOT FOUND'}, 404
    

    #Admin DELETE client details by ID
    @jwt_required
    @internal_required
    def delete(self,id):
        qry=Costumers.query.get(id)

        if qry is None:
           return  {'status': 'NOT FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return marshal(qry, Costumers.response_fields), 200

    def options(self,id):
        return {'status': 'OK'},200

class adminList(Resource):
    
    #Admin GET ALL client details as LIST
    @jwt_required
    @internal_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('p', location='args', type=int,default=1)  
        parser.add_argument('rp', location='args', type=int, default=25)
        args=parser.parse_args()

        qry=Costumers.query

        offset=(args['p']*args['rp'])-args['rp']

        rows=[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Costumers.response_fields))
        return rows,200

    def options(self):
        return {'status': 'OK'},200

class RegisterResource(Resource):

    def __init__(self):
        pass
    
    #Client(New User) POST his detail through Register Form
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument("client_name", location="args", required=True)
        parser.add_argument("client_password", location="args", required=True)
        parser.add_argument('full_name',location="args", required=True)
        parser.add_argument('telp',location="args", required=True)
        parser.add_argument('email',location="args", required=True)
        parser.add_argument('kota',location="args", required=True)
        args=parser.parse_args()
        
        biaya=get_rajaongkir(ongkir_host, ongkir_key)

        #Clent input name of city but this function with convert it to city id and store it to database
        for i in biaya['rajaongkir']['results']:
            if i['city_name'].lower()==args['kota'].lower():
                id_kota=i['city_id']

        #check whether the username and email entered already existed in database or not
        qry_username=Costumers.query.filter_by(client_name=args['client_name']).first()
        qry_email=Costumers.query.filter_by(email=args['email']).first()
        result_username=marshal(qry_username, Costumers.response_fields)
        result_email=marshal(qry_email, Costumers.response_fields)
        
        #encode password to be hidden using hashlib
        hidden_password=hashlib.md5(args['client_password'].encode()).hexdigest()
        if result_username['client_name'] == args['client_name'] or result_email['email'] == args['email']:
            return {'status':'Username or Email is already taken'}, 403
        
        register=Costumers(args['client_name'], hidden_password, args['full_name'],args['telp'],args['email'],id_kota)
        db.session.add(register)
        db.session.commit()
        return {'status':'Registration Success'},200
    
    def options(self):
        return {'status': 'OK'},200




#ENDPOINTS
api.add_resource(ClientResource, '','/<int:id>')
api.add_resource(ClientAdmin, '','/admin/<int:id>')
api.add_resource(adminList, '','/list')
api.add_resource(RegisterResource, '','/register')
    
