from flask import Flask , request
import json,logging
from logging.handlers import RotatingFileHandler
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os 
import json
from datetime import timedelta
from functools import wraps
from flask import Flask, request 
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims,create_access_token
from flask_cors import CORS, cross_origin

app=Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"]='SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(days=1)
jwt=JWTManager(app)

app.config["APP_DEBUG"]=True

try:
    env=os.environ.get("FLASK_ENV", "development")
    if env=="testing":
        app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:@localhost/TEST_DATABASE'
    else:
        app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:@localhost/REAL_DATABASE'
except Exception as e:
    raise e

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
migrate= Migrate(app, db)
manager=Manager(app)
manager.add_command('db', MigrateCommand)
db.create_all()


def internal_required(fn):
    @wraps(fn)
    def wrapper (*args,**kwargs):
        verify_jwt_in_request()
        claims=get_jwt_claims()
        try:
            if not claims['jabatan']:
                pass
        except:
            return {'status':'FORBIDDEN', 'message':'Administrator Only'}, 403
        else:
            return fn(*args,**kwargs)
    return wrapper

from blueprints.konsumen.resources import bp_costumer
from blueprints.login.__init__ import bp_login
from blueprints.produk.resources import bp_produk
from blueprints.belanja.resources import bp_belanja

app.register_blueprint(bp_costumer, url_prefix="/user")
app.register_blueprint(bp_belanja, url_prefix="/shop")
app.register_blueprint(bp_login, url_prefix="/login")
app.register_blueprint(bp_produk, url_prefix="/products")


@app.after_request
def after_request(response):
    if response.status_code==200:
        try:
            requestData=request.get_json()
        except Exception as e:
            requestData= request.args.to_dict()
        app.logger.info("REQUEST_LOG\t%s",
            json.dumps({ 
            'status_code': response.status_code,
            'method' :request.method,
            'code':response.status, 
            'uri':request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        try:
            requestData=request.get_json()
        except Exception as e:
            requestData= request.args.to_dict()
        app.logger.warning("REQUEST_LOG\t%s",
            json.dumps({ 
            'status_code': response.status_code,
            'method' :request.method,
            'code':response.status, 
            'uri':request.full_path,
            'request': requestData,
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response
# @app.after_request
# def after_request(response):
#     if response.status_code==200:
#         try:
#             requestData=request.get_json()
#         except:
#             requestData=request.args.to_dict()
#         app.logger.info('REQUEST_LOG\t%s', json_dumps({
#             'status_code':response.status_code,
#             'method':request.method,
#             'code':response.status,
#             'uri':request.full_path,
#             'request':requestData,
#             'response':json.loads(response.data.decode('utf-8'))
#             }))
#     else:
#         try:
#             requestData=request.get_json()
#         except:
#             requestData=request.args.to_dict()
#         app.logger.info(json.dumps({
#             'status_code':response.status_code,
#             'method':request.method,
#             'uri':request.full_path,
#             'code':response.status,
#             'request':requestData,
#             'response': json.loads(esponse.data.decode('utf-8'))
#             }))
#     return response