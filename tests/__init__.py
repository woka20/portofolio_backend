import pytest, json,logging
from app import app
from flask import Flask,request
from app import cache
from blueprints import app, db
from blueprints.konsumen.model import Costumers
import hashlib

def reset_db():
    db.drop_all()
    db.create_all()

    client=Costumers("admin", "woka",'Yudi','098765678','ansan@mantap.com',23,)
    db.session.add(client)
    db.session.commit()
    hiden=hashlib.md5('non-woka'.encode()).hexdigest()

    client=Costumers("non-admin", hiden,'Bambang','098765678','weleh@mantap.com',23)
    db.session.add(client)
    db.session.commit()


@pytest.fixture
def client(request):
    return app.test_client(request)

def create_token(isinternal=True):
    if isinternal:
        cachename='test-internal-token'
        data={
            'client_name':'admin',
            'client_password':'woka'
            
        }
    else:
        cachename= 'test-noninternal-token'
        data={
            'client_name':'non-admin',
            'client_password':'non-woka'
        }
    
    token=cache.get(cachename)
    
    if token is None:
        # data={
        #     'client_name':'admin',
        #     'client_password':'woka'
        # }
        req=app.test_client(request)
        res=req.get('/login',
           query_string=data
        )
           
        res_json=json.loads(res.data)
        logging.warning('RESULT: %s', res_json)
        
        if res.status_code==200:
           assert res.status_code==200
           cache.set(cachename, res_json['token'], timeout=60)
           return res_json['token']
        else:
            pass
    else:
        return token
