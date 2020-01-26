import json
from . import app,client, reset_db,create_token
import hashlib
import unittest
from unittest.mock import patch
from blueprints.konsumen.resources import get_rajaongkir
from blueprints.belanja.resources import post_rajaongkir
import requests
from unittest import mock
import base64


#Mocking GET RajaOngkir
def mocked_requests_get(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.status_code

		if args[0] == "https://api.rajaongkir.com/starter/city":
			return MockResponse({"city_id": 23,"city_name": "Bandung"}, 200)

#Mocking POST RajaOngkir
def mocked_requests_post(*args, **kwargs):
		class MockResponse():
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.status_code

		if args[0] == "https://api.rajaongkir.com/starter/cost":
			return MockResponse({"Biaya":40000}, 200)

#===============================================================================================================
#REGISTER and LOGIN

class TestClient():
    reset_db()


    #TEST REGISTER [POST] DI WEBSITE
    def test_post_register_valid(self,client):
       
        data=dict(
            client_name='waduh',
            client_password='rantang',
            full_name='Yudi',
            telp='098765678',
            email='hu@mantap.com',
            kota='Bandung',
        )

        res= client.post('user/register',query_string=data)

        res_json=json.loads(res.data)
        assert res.status_code==200

   

     #TEST REGISTER [POST] IN WEBSITE WITH EXISTED USERNAME  
    def test_post_register_invalid(self,client):
       
        data=dict(
            client_name='non-admin',
            client_password='non-woka',
            full_name='Yudi',
            telp='098765678',
            email='halo@mantap.com',
            kota='Bandung',
        )

        res= client.post('user/register',query_string=data)

        res_json=json.loads(res.data)
        assert res.status_code==403


    #TEST LOGIN [GET] IN WEBSITE AS ADMIN
    def test_admin_valid(self,client):
        token=create_token()

        data=dict(
            client_name='admin',
            client_password='woka',
    
        )
        
        res= client.get('/login',
            query_string=data,
            headers={'Authorization':'Bearer ' + token},
            content_type='application/json'
        )
    
        assert res.status_code==200

    #TEST LOGIN [GET] IN WEBSITE AS NON-ADMIN
    def test_admin_invalid(self,client):
        token=create_token(False)

        data=dict(
            client_name='non_admin',
            client_password='non-woka',
    
        )
        if token is None:
            res= client.get('/login',
            query_string=data,
            content_type='application/json')
            
            assert res.status_code==403
    
     

    #Client GET His Detail From Database 
    def test_external_get_customer(self,client):
        token=create_token(False)

        res= client.get('/user/2',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    #Client Fail To GET Detail Other Customer From Database 
    def test_external_fail_get_other_customer(self,client):
        token=create_token(False)

        res= client.get('/user/3',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==403
    
     #Client UPDATE His Own Detail From Database 
    def test_external_update_customer(self,client):
        token=create_token(False)

        data={
            'client_name': "sadewa",
            'client_password':"ayam",
            'full_name':"Sadewa Ayam",
            'telp':"08999765433",
            'email':"sadewa@jtn.com",
            'kota':"Malang",
        }

        res= client.put('/user/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
      #Client UPDATE His Own Detail From Database Without Any New Input
    def test_external_update_customer_without_input(self,client):
        token=create_token(False)

        data={"full_name": "",
              "telp": "",
              "email": "",
              "kota":""
        }

        res= client.put('/user/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    #Admin POST New Customer To Database
    def test_admin_add_customer(self,client):
        token=create_token()

        data={
            'client_name': "atta",
            'client_password':"gledek",
            'full_name':"Atta Gledek",
            'telp':"085758934521",
            'email':"atta@management.com",
            'kota':"Jakarta Barat",
        }

        res= client.post('/user/admin/4',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    def test_admin_register_same_email(self,client):
        token=create_token(True)

        data=dict(
            client_name='atta',
            client_password='rantang',
            full_name='Yudi',
            telp='098765678',
            email='atta@management.com',
            kota='Bandung',
        )
        if token is None:
            res= client.post('/user/admin/5',
            json=data,
            content_type='application/json')
            
            assert res.status_code==403
    
    #Admin GET customer data list
    def test_admin_get_customer(self,client):
        token=create_token()

        res= client.get('/user/list',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
   
     #Admin GET customer data by ID
    def test_admin_get_customer_by_id(self,client):
        token=create_token()

        res= client.get('/user/admin/3',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

     #Admin UPDATE customer data by ID
    def test_admin_update_customer(self,client):
        token=create_token()

        data={
            'client_name': "gledek",
            'client_password':"atta",
            'full_name':"Gledek Atta",
            'telp':"085758934526",
            'email':"atta@root.com",
            'kota':"Jakarta Selatan",
        }

        res= client.put('/user/admin/4',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

     #Admin UPDATE customer data Without New Input
    def test_admin_update_customer_without_input(self,client):
        token=create_token()

        data={'telp':"",
            'email':"atta1@root.com"}

        res= client.put('/user/admin/4',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

     #Admin DELETE customer data 
    def test_admin_delete_customer(self,client):
        token=create_token()


        res= client.delete('/user/admin/1',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200


    #=======================================================================================================
    #ACCESS PRODUCT 
    

     #Admin POST New PREMIUM(Brand New Product) Product
    def test_admin_add_product(self,client):
        token=create_token()

        data={
            'nama_produk': "RG Wing Gundam Zero EW",
            'category':"Real Grade",
            'harga':400000,
            'stok':5,
            'berat':2000,
            'gambar':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152536-60294.jpg",
            'preview_1':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152550-61824.jpg",
            'preview_2':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152601-39981.jpg",
            'preview_3':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152923-96005.jpg",
            'description':"The Wing Gundam Zero is the first New Mobile Report Gundam Wing: Endless Waltz suit to appear in RG! Its wings, designed for atmospheric reentry, are modeled as layered ablative heat absorption panels, and a lively, detailed sculpts combined with flexible positioning of each subwing create a voluminous, almost angelic span. "
        }

        res= client.post('/products/premium/1',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    #Admin POST an existed PREMIUM(Brand New Product) Product
    def test_admin_add_existed_product(self,client):
        token=create_token()

        data={
            'nama_produk': "RG Wing Gundam Zero EW",
            'category':"Real Grade",
            'harga':400000,
            'stok':5,
            'berat':2000,
            'gambar':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152536-60294.jpg",
            'preview_1':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152550-61824.jpg",
            'preview_2':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152601-39981.jpg",
            'preview_3':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152923-96005.jpg",
            'description':"The Wing Gundam Zero is the first New Mobile Report Gundam Wing: Endless Waltz suit to appear in RG! Its wings, designed for atmospheric reentry, are modeled as layered ablative heat absorption panels, and a lively, detailed sculpts combined with flexible positioning of each subwing create a voluminous, almost angelic span. "
        }

        res= client.post('/products/premium/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==403

    #Admin UPDATE data of PREMIUM(Brand New Product) Product    
    def test_admin_update_product(self,client):
        token=create_token()

        data={
            'nama_produk': "HGBD Gundam Love Phantom",
            'category':"High Grade",
            'harga':300000,
            'stok':3,
            'berat':1700,
            'gambar':"https://na.gundam.info/content/dam/gundam/gundaminfo/jp/image/news/180731_gbd/hobby_banner.jpg",
            'preview_1':"https://na.gundam.info/content/dam/gundam/gundaminfo/jp/image/news/180731_gbd/phantom4.jpg.thumb.300.300.png",
            'preview_2':"https://na.gundam.info/content/dam/gundam/gundaminfo/jp/image/news/180731_gbd/phantom1.jpg.thumb.300.300.png",
            'preview_3':"https://na.gundam.info/content/dam/gundam/gundaminfo/jp/image/news/180731_gbd/phantom3.jpg.thumb.300.300.png",
            'description':"The Gundam Love Phantom, used by the diver Magee from Gundam Build Fighters, gets a High Grade Build Custom! Using the back of the Noir Striker, the model was given a completely new mold, that allows a good range of action and movement. The characteristic heart shape on the forehead and wing cannons are clearly visible, and it comes with its topical scythe too."
        }

        res= client.put('/products/premium/1',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
   
   #Admin UPDATE data of PREMIUM(Brand New Product) Product Without New Input
    def test_admin_update_product_without_input(self,client):
        token=create_token()

        data={}

        res= client.put('/products/premium/1',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    #Admin GET Product By ID
    def test_admin_get_product_by_id(self,client):
        token=create_token()

        res= client.get('/products/premium/1',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    

    #Non-Admin POST new PELAPAK(Product sold by external Client) Product 
    def test_external_add_product(self,client):
        token=create_token(False)

        data={
            'nama_produk': "RG Zeta Gundam",
            'category':"Real Grade",
            'harga':200000,
            'stok':1,
            'berat':2000,
            'gambar':"https://www.1999.co.jp/itbig19/10197160.jpg",
            'preview_1':"https://www.1999.co.jp/itbig19/10197160a.jpg",
            'preview_2':"https://www.1999.co.jp/itbig19/10197160a5.jpg",
            'preview_3':"https://www.1999.co.jp/itbig19/10197160z11.jpg",
            'description':"As its 10th anniversary of RG series you should aggregating the technology that can have, the pursuit of real, finally Zeta Gundam appeared"
        }

        res= client.post('/products/used/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    #Just Add New Product
    def test_external_add_product_2(self,client):
        token=create_token(False)

        data={
            'nama_produk': "RG Destiny Gundam",
            'category':"Real Grade",
            'harga':200000,
            'stok':1,
            'berat':2000,
            'gambar':"https://www.1999.co.jp/itbig19/10197160.jpg",
            'preview_1':"https://www.1999.co.jp/itbig19/10197160a.jpg",
            'preview_2':"https://www.1999.co.jp/itbig19/10197160a5.jpg",
            'preview_3':"https://www.1999.co.jp/itbig19/10197160z11.jpg",
            'description':"As its 10th anniversary of RG series you should aggregating the technology that can have, the pursuit of real, finally Zeta Gundam appeared"
        }

        res= client.post('/products/used/3',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

  
    def test_external_update_product(self,client):
        token=create_token(False)

        data={
            'nama_produk': "HG Gundam Barbatos Lupus",
            'category':"High Grade",
            'harga':200000,
            'stok':1,
            'berat':1800,
            'gambar':"https://www.1999.co.jp/itbig40/10402215.jpg",
            'preview_1':"https://www.1999.co.jp/itbig40/10402215a.jpg",
            'preview_2':"https://www.1999.co.jp/itbig40/10402215a4.jpg",
            'preview_3':"https://www.1999.co.jp/itbig40/10402215b3.jpg",
            'description':"Gundam Tetsuhanadan that crescent-Augustine uses. Through a number of fights, it became the new figure is renovated by Teiwazu of technology. Each armed have also been strengthened. One machine of Gundam frame that was used for about 300 years ago [misfortune Festival warfare]"
        }

        res= client.put('/products/used/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

   #Non-Admin UPDATE his own PELAPAK(Product sold by external Client) Product Without Input
    def test_external_update_product_without_input(self,client):
        token=create_token(False)

        data={"nama_produk": "",
              "category": "",
              "harga":0,
              "stok":0,
              "berat":"",
              "gambar":"",
              "preview_1":"",
              "preview_2":"",
              "preview_3":"",
              "description":"",
        }

        res= client.put('/products/used/2',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

   #All Product By Id
    def test_external_get_product_by_id(self,client):
        

        res= client.get('/products/used/1',
        content_type='application/json')
            
        assert res.status_code==200


     #All GET PELAPAK(Product sold by external Client) Product List
    def test_get_product_all(self,client):

        res= client.get('/products/list',
        content_type='application/json')
            
        assert res.status_code==200

    def test_admin_add_product_3(self,client):
        token=create_token()

        data={
            'nama_produk': "RG Wing Gundam Zero EW",
            'category':"Real Grade",
            'harga':400000,
            'stok':5,
            'berat':2000,
            'gambar':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152536-60294.jpg",
            'preview_1':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152550-61824.jpg",
            'preview_2':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152601-39981.jpg",
            'preview_3':"https://na.gundam.info/content/dam/gundam/gundaminfo/old/na/image/thumbnail/2014/12/25/20141225152923-96005.jpg",
            'description':"The Wing Gundam Zero is the first New Mobile Report Gundam Wing: Endless Waltz suit to appear in RG! Its wings, designed for atmospheric reentry, are modeled as layered ablative heat absorption panels, and a lively, detailed sculpts combined with flexible positioning of each subwing create a voluminous, almost angelic span. "
        }

        res= client.post('/products/premium/1',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    
    def test_internal_update_product_without_input(self,client):
        token=create_token(True)

        data={"nama_produk": "",
              "category": "",
              "harga":0,
              "stok":0,
              "berat":0,
              "gambar":"",
              "preview_1":"",
              "preview_2":"",
              "preview_3":"",
              "description":"",
        }

        res= client.put('/products/premium/3',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
        
    def test_internal_update_user_product_without_input(self,client):
        token=create_token(True)

        data={"nama_produk": "",
              "category": "",
              "harga":0,
              "stok":0,
              "berat":0,
              "gambar":"",
              "preview_1":"",
              "preview_2":"",
              "preview_3":"",
              "description":"",
        }

        res= client.put('/products/used/11',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    #=============================================================================================================
    # SHOPPING CART

     #Client (Non-admin) POST Order To Cart 
    def test_external_add_shopping_cart(self,client):
        token=create_token(False)

        data=dict(
            product_id=2,
            kurir="jne",
            quantity=1,
        )

        res= client.post('/shop/cart',
        query_string=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_external_add_shopping_cart_exceeds_stock(self,client):
        token=create_token(False)

        data=dict(
            product_id=2,
            kurir="jne",
            quantity=5,
        )

        res= client.post('/shop/cart',
        query_string=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==403

    def test_external_add_shopping_cart_exceeds_weight(self,client):
        token=create_token(False)

        data=dict(
            product_id=2,
            kurir="jne",
            quantity=5,
        )

        res= client.post('/shop/cart',
        query_string=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==403


    #Client (Non-admin) GET his checkout detail 
    def test_get_detail_shopping_checkout(self,client):
        token=create_token(False)

        res= client.get('/shop/checkout',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    #Client (Non-admin) GET his shopping cart detail
    def test_get_detail_shopping_cart(self,client):
        token=create_token(False)

        res= client.get('/shop/cart',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    #Client (Non-admin) POST Transfer Receipt
    def test_update_bukti_pembayaran(self,client):
        token=create_token(False)
     
        with open("dummy.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string2="data:image/jpg;base64,"+encoded_string.decode('utf-8')
        data={'id':1,
        'bukti_pembayaran': encoded_string2}

        res= client.put('/shop/confirm/1',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200
    
    #Admin Update Client Payment Status 
    def test_admin_update_status_pembayaran(self,client):
        token=create_token()
        data={'id':1,
              'payment': "LUNAS"}

        res= client.put('/shop/checkout',
        json=data,
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_get_shop_cart(self,client):
        token=create_token(False)
        
        res= client.get('/shop/confirm/1',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200


    #============================================================================================================    
    #   DELETE PRODUCT   

    def test_admin_delete_product_by_id(self,client):
        token=create_token()

        res= client.delete('/products/premium/1',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_external_delete_product_by_id(self,client):
        token=create_token(False)

        res= client.delete('/products/used/3',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

#====================================================================================================================
#OPTIONS
    def test_options_konsumen(self,client):
        token=create_token(False)


        res= client.options('/user/list',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_options_register(self,client):
        token=create_token(False)


        res= client.options('/user/register',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_options_clientAdmin(self,client):
        token=create_token(False)


        res= client.options('/user/admin/2',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_options_clientResource(self,client):
        token=create_token(False)


        res= client.options('/user/2',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    
    def test_options_shopCart(self,client):
        token=create_token(False)


        res= client.options('/shop/cart',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_options_confirmID(self,client):
        token=create_token(False)


        res= client.options('/shop/confirm/1',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

    def test_options_checkout(self,client):
        token=create_token(False)


        res= client.options('/shop/checkout',
        headers={'Authorization':'Bearer ' + token},
        content_type='application/json')
            
        assert res.status_code==200

#=======================================================================================================================
#TEST API RAJAONGKIR
class OngkirTest(unittest.TestCase):
    #METHOD GET
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_rajaongkir_api(self, mock_get):
        mock_get.return_value.status_code=200
        ongkir_host="https://api.rajaongkir.com/starter"
        ongkir_key="fb63156a683784f4edbd8f23ea73a4a3"
        response=get_rajaongkir(ongkir_host,ongkir_key)
        
        assert response==200

    #METHOD POST
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_post_rajaongkir_api(self, mock_post):
        mock_post.return_value.status_code=200
        ongkir_host="https://api.rajaongkir.com/starter"
        ongkir_key="fb63156a683784f4edbd8f23ea73a4a3"
        response=post_rajaongkir(ongkir_host,256, 23, 1800, "jne",ongkir_key)
        
        assert response==200




   