# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:19:22 2021

@author: chintak
"""
import requests
import cx_Oracle
import config
import json
#import mergequery
url='https://reqres.in/api/products'
# print(mergequery.MergeQuery)
# merQ = ('mergequery.MergeQuery')
# print(merQ)

resp=requests.get(url)
json_data=resp.json()
total_Pages = json_data['total_pages']
total_Pages = total_Pages + 1

MyQ = ('Insert into im.test_product(ID, NAME, YEAR, COLOR, PANTONE_VALUE) '
    'values(:ID, :NAME, :YEAR, :COLOR, :PANTONE_VALUE)')
resultresp=[]
for page in range(1,total_Pages):
    url = 'https://reqres.in/api/products?page=%s'%page
    json_data = requests.get(url).json()
    
    jsonobject=json.dumps(json_data)
    jsonObjectToString=json.loads(jsonobject)
    for value in jsonObjectToString["data"]:
        products= value["id"],value["name"],value["year"],value["color"],value["pantone_value"]
        resultresp.append(products)
    print(resultresp)
     
connection = None
try:
    connection = cx_Oracle.connect(
        config.username,
        config.password,
        config.dsn,
        encoding=config.encoding
        )
    print(connection.version)
    # print(resultresp)
    connection.autocommit=True
    
    with connection.cursor() as cur:
      #cur.execute('create table product_src (ID Number(10) not null primary key,Name Varchar2(50),Year Number(4),color varchar2(30),pantone_value varchar2(40)')
     
      MyQ = ('Insert into im.test_product(ID, NAME, YEAR, COLOR, PANTONE_VALUE) '
            'values(:ID, :NAME, :YEAR, :COLOR, :PANTONE_VALUE)')
      print(MyQ)
      cur.executemany(MyQ, resultresp)
      
   #  with connection.cursor() as cur:
   #      #Mymerge = mergequery.MergeQuery
   #     # Mymerge = ('update test_product set year=3000 where id= :myid')
   #    #  print('Pratap')
        
   # #     cur.execute(Mymerge, myid=3)
   #       cur.callproc('myMergeq')
   #       connection.autocommit=True
        
    connection.commit()
except cx_Oracle.Error as error:
    print(error)
    
     
finally:
     if connection:
         connection.close()