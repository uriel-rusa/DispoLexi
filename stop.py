from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#PARTE PARA CREAR LISTA DE STOP WORDS
'''
file = open('stop_words_spanish01.txt','r', encoding="utf-8")
text = file.read()
file.close()
tokens = word_tokenize(text)
print(tokens)
print("FIN DE LISTA")


stop_words = set(stopwords.words('spanish')) 
for x in stop_words:
	if not x in tokens:
		tokens.append(x)

tokens.sort()

for word in tokens:
	appendFile = open("stop_words.txt", 'a')
	appendFile.write("\n" + word) #Se ecribe la palabra separada por un espacio en el nuevo
'''		




#PARTE PARA PRUEBA CON EL STOP_WORDS
file = open('stop_words.txt','r', encoding="latin-1")
text = file.read()
file.close()
tokens = word_tokenize(text)
print(tokens)
print("FIN DE LISTA")


stop_words = set ('')
for x in tokens:
	stop_words.add(x)
print(stop_words)
print(len(stop_words))

for word in stop_words:
	appendFile = open("stop_words_utimo.txt", 'a')
	appendFile.write("\n" + word) #Se ecribe la palabra separada por un espacio en el nuevo

counter = 0
for x in tokens:
	for z in tokens: 
		if x == z:
			counter += 1
	if counter >=2:
		print("La palabra: ",x," está ", counter, " en stop_words.")
	counter = 0