from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
import hashlib
from  ..konsumen.model import Costumers

bp_login=Blueprint("login", __name__)
api=Api(bp_login, catch_all_404s=True)

#create token for all user who want access the website
class CreateToken(Resource):
    #get token for all
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument("client_name", location="args", required=True)
        parser.add_argument("client_password", location="args", required=True)
        args=parser.parse_args()
        
        #If admin, if this condition fulfilled, admin can login immediately and access all feature
        if args["client_name"]=="admin" and args["client_password"]=="woka":
            token=create_access_token(identity=args["client_name"], user_claims={"jabatan":"admin"})
            return {"token":token},200
        #if not admin, the input client_name/username and client_password/password should be already in dtaabase to login
        elif args["client_name"]!="admin" and args["client_password"]!="woka":
            qry=Costumers.query.filter_by(client_name=args['client_name']).first()
            x=hashlib.md5(args['client_password'].encode()).hexdigest()
            if qry.client_name==args['client_name'] and qry.client_password == x:
                clientData=marshal(qry, Costumers.jwt_claims_fields)
                
                token=create_access_token(identity=args['client_name'], user_claims=clientData)
                return {"clientData":clientData, 'token':token}, 200
            
            else:
                return {'status':'You cannot login. Username or password invalid or Register yourself first'}, 403
    

#ENDPOINTS
api.add_resource(CreateToken, '')
