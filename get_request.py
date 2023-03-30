# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 14:47:33 2021

@author: gabriel.ferraz
"""

import pandas as pd
import requests as req
import json

df = pd.read_csv(r'C:\ATPx\cep\qualocep_endereco.csv')
df.head(10)
list(df.columns)
df['endereco'] = df['tipo_logradouro'].astype(str ).replace('nan','') + " " + df['logradouro']
df['endereco'] = df['endereco'].fillna("").apply(lambda x: x.strip())

#df_teste = df.head(1000) 

#exemplo get
def phonetic(x):
    try:
        doc = str(x)
        phonetic_txt = req.get('https://phonetic.atfunctions.com/api/phonetic/process/'+doc+'/?IAMKEY=6E75B351F4E14216CDB3769FE0CE016A1CE27A82CDD6FA7DF6476437BF574209')
        try:
            jsonresposta = json.loads(phonetic_txt.text)
            resposta = jsonresposta
            resposta = resposta['objectResult']['phoneticText'].split(';')[1]
        except:
               resposta = "erro"
    except:
           resposta = "erro"

    #time.sleep(1)  
    return(resposta)
       


phon_series = df['endereco'].apply(phonetic)


