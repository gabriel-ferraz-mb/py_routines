# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 10:43:12 2023

@author: gabri
"""
import psycopg2
import sqlalchemy    
from sqlalchemy import create_engine 

user = 'ferraz'
password = '3ino^Vq3^R1!'
host = 'vps40890.publiccloud.com.br'
port = 5432
database = 'carbon'

engine = create_engine(
         url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
             user, password, host, port, database
         )
     )
 
 
if not engine.dialect.has_schema(engine, 'monitoramento'):
    engine.execute(sqlalchemy.schema.CreateSchema('monitoramento'))
 
conn = psycopg2.connect("host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
     host, port, database, user, password))
cur = conn.cursor()
ct_query = "CREATE TABLE monitoramento.vazio_sanitario (estado varchar, data varchar);"
# # q = "DROP TABLE research.conab_base;"
# # cur.execute(q)
cur.execute(ct_query.lower())
conn.commit()
csv_file_name = 'vazio_sanitario.csv'
insert = "COPY monitoramento.vazio_sanitario FROM STDIN DELIMITER ';' CSV HEADER"
cur.copy_expert(insert, open(csv_file_name, "r"))
conn.commit()
conn.close()
