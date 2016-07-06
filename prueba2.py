import os
import re

dir_ham = os.getcwd()+"/enron1/ham"
dir_spam = os.getcwd()+"/enron1/spam"

lstDir = os.walk(dir_ham)

print lstDir

contador = 0

for i in lstDir:
 	contador+=1
 	print len(i[2])

print contador

# lstDir = os.walk(dir_spam)

# for i in lstDir:
# 	print len(i[2])

# patron_nln = re.compile('\W')

# patron_nn = re.compile('\d')

# palabra = "444"

# for i in patron_nn.findall("444"):
# 	nuevo = "".join(palabra.split(i))

# print nuevo
# print len(nuevo)