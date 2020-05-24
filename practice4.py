import requests
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords    
import re
#f = open("CS372_HW3_output_20160638.csv", "w")
#sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
#print(sentences[0])
#print(stopwords.words('english') )
aa=[[3,5],[4,5]]
for a, b in aa:
    print(a)