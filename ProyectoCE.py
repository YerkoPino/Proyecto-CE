from pyevolve import *
import os
import re

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

for term in lista_term:
	if lista_term[term]["dfs"]>=0.568870803164:
		print term,lista_term[term]["dfs"]