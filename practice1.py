from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
lm = WordNetLemmatizer() 
entries = nltk.corpus.cmudict.entries()
for word, pron in entries:
    if(word == "tear"):
        print(pron)
for syn in wn.synsets("tear"):
    print( syn, syn.definition())
#print(wn.synsets("tear"))