from flask import Blueprint,request, render_template,Flask

file_bukti=request.files["dummy.jpg"]
print(file_bukti.read())


# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.post("http://httpbin.org/post", data=payload)
# print (r.json())
# # stocks = {
# #         'IBM': 146.48,
# #         'MSFT':44.11,
# #         'CSCO':25.54
# #     }
    
# # #print out all the keys
# # for c in stocks:
# #     print(c)
    
# # #print key n values
# # for k, v in stocks.items():
# #     print(k.replace("'",""))