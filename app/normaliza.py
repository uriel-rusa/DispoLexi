import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import io  
#word_tokenize accepts a string as an input, not a file. 
stop_words = set(stopwords.words('spanish')) 
file1 = open("tecnologia.txt") 
text = file1.read()# Use this to read file content as a stream: 
for x in text:
	text.replace('"','')
# convirtiendo en palabras
tokens = word_tokenize(text)
# convertir a minúsculas
tokens = [w.lower() for w in tokens]
# prepare a regex para el filtrado de caracteres
re_punc = re.compile('[%s]' % re.escape(string.punctuation))
# eliminar la puntuación de cada palabra
stripped = [re_punc.sub('', w) for w in tokens]
# eliminar los tokens restantes que no estén en orden alfabético
words = [word for word in stripped if word.isalpha()]

 
for r in words: 
    if not r in stop_words: 
        appendFile = open('filteredtext.txt','a') 
        appendFile.write(" "+r) 
        appendFile.close()

