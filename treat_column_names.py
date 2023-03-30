csv# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 14:47:33 2021

@author: gabriel.ferraz
"""

import pandas as pd
from unidecode import unidecode

path = r'C:\ATPx\dinamica_producao\satveg_planilha_ndvi.csv'
name = path.split("\\")[-1].split(".")[0]
finalname = name + "_correct"
df = pd.read_csv(path, ";")
df.head(10)
df["ndvi"] = df["ndvi"].str.replace(',', '.')
df["pre_filtro"] = df["pre_filtro"].str.replace(',', '.')
columns = list(df.columns)
#columns = columns[0].split(";")
columnstreat = [each_string.lower() for each_string in columns]
columnstreat = [unidecode(each_string) for each_string in columnstreat]
finalcolumns = []
for string in columnstreat:
    new_string = string.replace(".", "").replace(" ", "_").replace(",", "").replace("-", "_").replace("/","_").replace("\\","_")
    finalcolumns.append(new_string)
    
dictionary = dict(zip(columns, finalcolumns))
dictionary
df.rename(dictionary, axis=1, inplace=True)

txtname = path.replace("csv","txt")
df.to_csv(txtname, sep ="\t", index = False)

