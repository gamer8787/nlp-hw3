from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
lm = WordNetLemmatizer()    
#f = open("CS372_HW3_output_20160638.csv", "w")
b= [0]*15
sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
escape = False
wantsen = []
accept_list = ["ADJ", "ADV", "NOUN", "VERB"]
for sen in sentences:
    for word in sen:
        if(word[0] == "tear"):
            sen2=[a for (a,b) in sen]    #word extract
            sen3=' '.join(sen2) 
            wantsen.append([word,sen3])
            break
for sen in wantsen[:50]:
    print(sen)
