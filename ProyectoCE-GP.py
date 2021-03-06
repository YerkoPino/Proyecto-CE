from pyevolve import *
from sklearn import svm
from time import time
import os
import re
import random

tiempo_inicial = time()

alpha = 0.5
mejor_fitness = -1
mejor_acc = -1
features = -1
features_cons = 100

conjunto = [None]*32
for i in range(32):
   aux = [None]*features_cons
   for j in range(features_cons):
      aux[j] = random.randint(0,1)
   conjunto[i] = aux

def borrar(cont):
   c=""
   for e in cont:
      if e.isalpha() or e==' ':
         c=c+e
   return c

dir_ham = os.getcwd()+"/enron1/ham"
dir_spam = os.getcwd()+"/enron1/spam"

patron_nln = re.compile('\W')
patron_nn = re.compile('\d')

id_file = 0

for i in os.walk(dir_ham):
   lista_ham = i[2]

for i in os.walk(dir_spam):
   lista_spam = i[2]

total_files = len(lista_spam) + len(lista_ham)

lista_term = {}

for nombre in lista_ham:
   
   archivo = open(dir_ham+"/"+nombre)
   contenido = archivo.read().split("\r\n")
   contenido = " ".join(contenido)
   contenido = borrar(contenido)
   contenido = contenido.split(" ")
   archivo.close()

   while '' in contenido:
      contenido.remove('')

   for term in contenido:
      if term in lista_term:
         if id_file in lista_term[term]:
            lista_term[term][id_file] +=1
         else:
            lista_term[term][id_file] = 1
      else:
         lista_term[term] = {}
         lista_term[term][id_file] = 1

   id_file += 1

for nombre in lista_spam:
   
   archivo = open(dir_spam+"/"+nombre)
   contenido = archivo.read().split("\r\n")
   contenido = " ".join(contenido)
   contenido = borrar(contenido)
   contenido = contenido.split(" ")
   archivo.close()

   while '' in contenido:
      contenido.remove('')

   for term in contenido:
      if term in lista_term:
         if id_file in lista_term[term]:
            lista_term[term][id_file] +=1
         else:
            lista_term[term][id_file] = 1
      else:
         lista_term[term] = {}
         lista_term[term][id_file] = 1

   id_file += 1

for term in lista_term:
   contador_c0t = 0
   contador_c1t = 0
   pct0 = 0.0
   pct1 = 0.0
   pntc0 = 0.0
   ptnc0 = 0.0
   pntc1 = 0.0
   ptnc1 = 0.0

   for file in lista_term[term]:
      if file<3672:
         contador_c0t += 1
      else:
         contador_c1t += 1

   pct0 = float(contador_c0t)/float(contador_c0t+contador_c1t)
   pct1 = float(contador_c1t)/float(contador_c0t+contador_c1t)

   pntc0 = 1.0-(contador_c0t/3672.0)
   ptnc0 = contador_c1t/1500.0

   pntc1 = 1.0-(contador_c1t/1500.0)
   ptnc1 = contador_c0t/3672.0

   dfs = (pct0/(pntc0+ptnc0+1))+(pct1/(pntc1+ptnc1+1))

   lista_term[term]["dfs"] = dfs

matriz_datos = [None]*total_files
for i in range(total_files):
   matriz_datos[i] = [0]*features_cons

columna = 0

for term in lista_term:
   if lista_term[term]["dfs"]>=0.512705948059:
      for file in lista_term[term]:
         if file!="dfs":
            matriz_datos[file][columna] = lista_term[term][file]
      columna += 1

entrenamiento = matriz_datos[0:2448]+matriz_datos[3672:4672]
validacion = matriz_datos[2448:3672]+matriz_datos[4672:5172]

clase_entr = [0]*2448+[1]*1000
clase_valid = [0]*1224+[1]*500

def gp_and(a,b):
   resultado = [None]*features_cons
   for i in range(features_cons):
      resultado[i] = a[i] and b[i]
   return resultado
def gp_or(a,b):
   resultado = [None]*features_cons
   for i in range(features_cons):
      resultado[i] = a[i] or b[i]
   return resultado
def gp_xor(a,b):
   resultado = [None]*features_cons
   for i in range(features_cons):
      resultado[i] = a[i] ^ b[i]
   return resultado
def gp_not(a):
   resultado = [None]*features_cons
   for i in range(features_cons):
      if not(a[i]):
         resultado[i] = 1
      else:
         resultado[i] = 0
   return resultado
def gp_juntar_centro(a,b): return a[50:100]+b[0:50]
def gp_juntar_extremo(a,b): return a[0:50]+b[50:100]
def obtener(): return conjunto[random.randint(0,31)]

def eval_func(chromosome):
   global mejor_fitness
   global mejor_acc
   global features

   code_comp = chromosome.getCompiledCode()

   evaluated = eval(code_comp)

   suma = 0
   for value in evaluated:
      if value==1:
         suma += 1

   if suma>0:

      entrenamiento_svm = [None]*3448
      for i in range(3448):
         entrenamiento_svm[i] = [0]*suma

      validacion_svm = [None]*1724
      for i in range(1724):
         validacion_svm[i] = [0]*suma

      col_valida = 0
      col_valida_svm = 0
      for value in evaluated:
         if value==1:
            for i in range(3448):
               entrenamiento_svm[i][col_valida_svm] = entrenamiento[i][col_valida]
            for i in range(1724):
               validacion_svm[i][col_valida_svm] = validacion[i][col_valida]
            col_valida_svm += 1
         col_valida += 1

      support = svm.SVC()
      support.fit(entrenamiento_svm,clase_entr)

      resultado = support.predict(validacion_svm)

      aciertos = 0

      for i in range(1724):
         if resultado[i]==clase_valid[i]:
            aciertos +=1

      fitness = alpha*(1.0-float(aciertos)/1724.0)+(1.0-alpha)*(float(suma)/float(features_cons))

      if fitness<mejor_fitness or mejor_fitness==-1:
         features = suma
         mejor_fitness = fitness
         mejor_acc = 1.0-float(aciertos)/1724.0

      return fitness
   else:
      return 0.5

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="ramped")
   genome.evaluator.set(eval_func)

   ga = GSimpleGA.GSimpleGA(genome)
   sqlite_adapter = DBAdapters.DBSQLite(identify="exgp")
   ga.setDBAdapter(sqlite_adapter)

   ga.setParams(gp_terminals       = ["obtener()"],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(20)
   ga.setMutationRate(0.08)
   ga.setCrossoverRate(0.8)
   ga.setPopulationSize(200)
   ga.evolve(freq_stats=1)

   tiempo_final = time()

   best = ga.bestIndividual()
   best.writeDotImage("best.jpg")
   print best
   print ""
   print "Mejor fitness:",mejor_fitness
   print "Error:",mejor_acc
   print "Features:",features
   print "Tiempo total:",(tiempo_final-tiempo_inicial)


if __name__ == "__main__":
   main_run()