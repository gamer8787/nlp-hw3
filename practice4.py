import requests
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords  
lm = WordNetLemmatizer()    
#f = open("CS372_HW3_output_20160638.csv", "w")
#sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
#print(len(sentences))
#print(stopwords.words('english') )
print("RoW:".lower())