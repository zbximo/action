# # %%
# import pymysql
#
# # %%
# db=pymysql.connect(host="localhost",user="diana",password="ava",database="tron")
#
# # %%
# cursor=db.cursor()
#
# # %%
# import requests
#
# # %%
# hjm=26465864
# while True:
#
#     x=requests.post('http://localhost:8090/wallet/gettransactioninfobyblocknum',json={
#
#     "num":hjm,
#     "visible":"True"
#
#     })
#     y=x.json()
#     for i in y:
#         if "contract_address" in i:
#             if i["contract_address"]=="TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
#                 cursor.execute('insert ignore into trade (tradehash) values (%s)',i["id"])
#                 db.commit()
#     hjm+=1
#     print(hjm)
#

import yaml

f = open('config.yaml', 'r')
data = yaml.load(f, Loader=yaml.FullLoader)
print(data['base_data']['inflect']['ip'])
