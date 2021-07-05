import numpy as np
from py2neo import Node,Relationship,Graph, database,NodeMatcher  
import time
import pandas as pd
graph=Graph()#Graph('bolt://neo4j@localhost:7687')
genes_list=pd.read_csv("Gen_list.txt",delimiter="\t",header=None)
genes_list=genes_list[0].tolist()

''' crear los 20244 genes de dorothea
for name in genes_list:
    graph.run("CREATE(:GEN{name:$name})",name=name)
se demoró un par de segundos
'''
genes=pd.read_csv(r"C:\Users\espin\OneDrive\Escritorio\MCI\SCRIPTS\dorothea_final.csv", delimiter="\t",header=None)
genes2=list(genes.to_records(index=False))

for tupla in genes2[3:]:
    graph.run("MATCH(a:GEN{name:$name}) MATCH(b:GEN{name:$name1}) CREATE (a)-[:REGULATES]->(b)",name=tupla[0],name1=tupla[1])


for tf in genes2[0:5]:
   print(tf[0],tf[1])
for tf in genes2[3:5]:
   print(tf[0],tf[1])

matcher = NodeMatcher(graph)


REGULATES = Relationship.type("REGULATES")

for tupla in genes2:
    existing_u1 = matcher.match("GEN").where(name=tupla1).first()
    existing_u2 = matcher.match("GEN").where(name=tupla2).first()
    graph.merge(existing_u1,"REGULATES", existing_u2)

for tupla in genes2:
    graph.run("MATCH (a:GEN) where a.name= x",x=tupla1).evaluate()
             MATCH (b:GEN) where b.name= y",y=tupla2)
    graph.run("CREATE  (a)-[REGULATES]->(b) RETURN a,b")
    
#merge (ori:GENE:TF{name:'ADNP'})
#merge(t:GENE{name:'ATF7IP'})
#CREATE(ori)-[:REGULATES]->(t);

for tf in genes2[0:5]:
   print(tf[0],tf[1])
y="ATF7IP"
query_string = "MATCH (a:GEN)  WHERE a.name = $y"
graph.run(query_string, {"y":y}).to_table()


query = "MATCH (a:GEN $params ) RETURN a AS GENES"
graph.run(query, params= {name:tupla1})

'''
create second label "TF"
match (n {id:desired-id})
set n :newLabel ESTA PARTE SI FUNCIONA TAL CUAL ESTA EL 7/6/2021
'''

tf=pd.read_csv(r"C:\Users\espin\OneDrive\Escritorio\MCI\SCRIPTS\TF_list.txt", delimiter="\t",header=None)
tf.head()
for gen in tf[0]:
    #print(gen)
    graph.run("MATCH(a:GEN{name:$name}) set a :TF ",name=gen)

res=pd.read_csv(r"C:\Users\espin\OneDrive\Escritorio\MCI\SCRIPTS\Ncounts2Syb_res.csv")
#### CORRER ESTA LINEA y ver si podemos crear para el experimetno todas las relaciones con los genes que cumplen ser mayor que 10 en el theshole
for i in range(0,len(res["Syb"])):
    if res["healthy"][i]>10:
        graph.run("MERGE(a:EXPERIMENT{code:$code,condition:$condition}) MERGE(b:TF{name:$tf}) CREATE (a)-[:DEG]->(b) ",code="GSM4462413",condition="Healthy", tf=res["Syb"][i])
    if res["Infected"][i]>10:
        graph.run("MERGE(a:EXPERIMENT{code:$code,condition:$condition}) MERGE(b:TF{name:$tf}) CREATE (a)-[:DEG]->(b)",code="GSM4462415",condition="Infected", tf=res["Syb"][i])

####



