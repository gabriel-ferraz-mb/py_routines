# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 11:26:33 2023

@author: gabri
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
pd.options.mode.chained_assignment = None
from unidecode import unidecode
#from sqlalchemy import create_engine
import urllib.request
from bs4 import BeautifulSoup

#builtwith.parse("https://www.conab.gov.br/info-agro/safras/progresso-de-safra")

fp = urllib.request.urlopen("https://www.conab.gov.br/info-agro/safras/progresso-de-safra")
bsObj = BeautifulSoup(fp, 'html.parser')
links = bsObj.find_all('a', href=True)
hrefList = []
for link in links:
    if 'Plantio e colheita' in link.text:
        hrefList.append(link['href'])

path = r'C:\Projetos\Research\\'
name = 'palntio_colheita.xlsx'
urllib.request.urlretrieve("https://www.conab.gov.br/" + hrefList[0], path + name)

conn = psycopg2.connect("host='186.202.136.178' port='5432' dbname='carbon' user='ferraz' password='$14EcZy2snd3'")
cur = conn.cursor()

# tableName = "research.conab_base"
# ct_query = "CREATE TABLE research.conab_base (Safra varchar, Safras varchar, Data varchar, Tocantins float, Maranhao float, Piaui float, Bahia float, Mato_Grosso float, Mato_Grosso_do_Sul float, Goias float, Minas_Gerais float, Sao_Paulo float, Parana float, Santa_Catarina float, Rio_Grande_do_Sul float, TODOS float);"
# # q = "DROP TABLE research.conab_base;"
# # cur.execute(q)
# cur.execute(ct_query.lower())

# with open(r'C:\Projetos\Research\CONAB_BASE.csv', 'r') as fin:
#     data = fin.read().splitlines(True)
#     #data = data[1:]
# with open(r'C:\Projetos\Research\CONAB_BASE_c.csv', 'w') as fout:
#     fout.writelines(data[1:])

# sqlstr = "COPY conab_base FROM STDIN DELIMITER ';' CSV"    
# d = open(r'C:\Projetos\Research\CONAB_BASE_c.csv', 'r')#.read().replace('.', ',') 
#cur.copy_expert(sqlstr, d)

# cur.copy_from(d, 'conab_base', sep=';')

csv_file_name = r'C:\Projetos\Research\CONAB_BASE_c.csv'
sql = "COPY research.conab_base FROM STDIN DELIMITER ';' CSV"
cur.copy_expert(sql, open(csv_file_name, "r"))

conn.commit()
conn.close()

#pd.set_option('display.max_rows', 200)
conab = pd.read_excel(path + name)
conab.set_axis(['A', 'B', 'C', 'D', 'E'], axis=1, inplace=True)

i, j = (conab.applymap(lambda x: str(x).startswith('Soja - Safra'))).values.nonzero()

year = str(conab.iloc[i, j]).split(' ')[-1]
safra = year.replace('/', '_')

soy = conab.iloc[i[0]+5:i[0]+19, j[0]:j[0]+4]

#soy.to_excel(r'C:\Projetos\Research\soy.xlsx')
soy.iloc[0,0] = 'uf'
soy.columns = soy.iloc[0]
soy.drop(index=soy.index[0], axis=0, inplace=True)
soy.drop(soy.columns[1],axis = 1, inplace = True)
#soy.set_axis(['UF', 'B', 'C', 'D', 'E'], axis=1, inplace=True)
soy['uf'] = soy['uf'].str.replace(' ','_').str.lower().apply(unidecode)
date1 = soy.columns[1:3][0]
date2 = soy.columns[1:3][1]

soy.set_axis(['UF', 'Y', 'Z'], axis=1, inplace=True)
soyT = soy.transpose()
soyT.columns = soyT.iloc[0]
soyT.drop(index=soyT.index[0], axis=0, inplace=True)
soyT['safra'] = safra
soyT['safras'] = year
soyT['data'] = ''
soyT.at['Y', 'data'] = date1.strftime('%d/%b').lower() 
soyT.at['Z', 'data'] = date2.strftime('%d/%b').lower() 
soyT.rename(columns = {'12_estados':'todos'}, inplace = True)
df = soyT

# columns = list(df.columns)
# columns = ["df." + x for x in columns if not str(x) == "nan"]

df["query"] = "('" + df.safra.astype(str) +"', '" +  df.safras.astype(str) + "', '" + df.data.astype(str) +\
    "', " + df.tocantins.astype(str) + ", " + df.maranhao.astype(str) + ", " + df.piaui.astype(str) +\
        ", " + df.bahia.astype(str) +", " + df.mato_grosso.astype(str) +\
            ", " + df.mato_grosso_do_sul.astype(str) +", " + df.goias.astype(str) +\
                ", " + df.minas_gerais.astype(str) +", " + df.sao_paulo.astype(str) +\
                    ", " + df.parana.astype(str) + ", " + df.santa_catarina.astype(str) +\
                        ", " + df.rio_grande_do_sul.astype(str) +", " + df.todos.astype(str)+\
                    ")"

a  = df["query"].tolist()
query = ", ".join(a)

query ="INSERT INTO research.conab_base (safra, safras, data, tocantins, maranhao, piaui, bahia, "+\
    "mato_grosso, mato_grosso_do_sul, goias, minas_gerais, sao_paulo, parana, santa_catarina, rio_grande_do_sul, todos" +\
    ") VALUES " + query
#print(query)

conn = psycopg2.connect("host='186.202.136.178' port='5432' dbname='carbon' user='ferraz' password='$14EcZy2snd3'")
cur = conn.cursor()
#ct_query = "CREATE TABLE public.conab_base (Safra varchar, Safras varchar, Data varchar, Tocantins float, Maranhao float, Piaui float, Bahia float, Mato_Grosso float, Mato_Grosso_do_Sul float, Goias float, Minas_Gerais float, Sao_Paulo float, Parana float, Santa_Catarina float, Rio_Grande_do_Sul float, TODOS float);"

cur.execute(query)
conn.commit()
conn.close()
