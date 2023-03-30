# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 10:22:07 2022

@author: gabriel.ferraz
"""


import pygeohash as pgh
import pandas as 


df = pd.read_csv(r'C:\ATPx\AT_Crop\amostras_total_cultura_pgh.csv', sep=';')
#df['geo_hash'] = df.apply(lambda x: pgh.encode(x.latitude, x.longitude), axis=1)
# =============================================================================
df['data_inicial'] = pd.to_datetime(df['data_inicial'], format = "%Y-%m-%d").dt.strftime('%Y/%m/%d')
# =============================================================================
# type(df['data_inicial'][0])
# df['data_inicial'] = df['data_inicial'].apply(lambda x: x.strftime('%Y/%m/%d'))
# =============================================================================
# =============================================================================

var = pgh.decode("855fb293fffffff")


df.to_csv(r'C:\ATPx\AT_Crop\amostras_total_cultura_pgh_dt.csv', sep=';', encoding='utf-8', index=False)

# coordinates = pgh.encode(-54.87, -16.34)
# print(coordinates)