import pandas as pd

df = pd.read_csv(r"C:\ATPx\Safe\sema_amb_csa_areas_embargadas_mt_poligonos_a.txt", sep = "\t")
columns = list(df.columns)
columns = ["df." + x for x in columns if not str(x) == "nan"]

df["query"] = "('" + df.gid.astype(str) +"', '" +  df.ano_desmat.astype(str) + "', '" + df.geom.astype(str) + "')"

a  = df["query"].tolist()
query = ", ".join(a)

query ="INSERT INTO public.sema (id, ano, geom) VALUES " + query
print(query)

with open(r"C:\ATPx\Safe\sema.txt" , "w") as text_file:
    text_file.write(query)
