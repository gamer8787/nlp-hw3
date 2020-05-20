from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
lm = WordNetLemmatizer()    
#f = open("CS372_HW3_output_20160638.csv", "w")
sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
escape = False
wantsen = []
accept_list = ["ADJ", "ADV", "NOUN", "VERB"]
for sen in sentences:
    escape = False
    for i in range(len(sen)):
        for j in range(i):
            if( sen[i][0] == sen[j][0] and sen[i][1] in accept_list and sen[j][1] in accept_list and sen[i][1]!=sen[j][1]
                    and (sen[i][0][0].islower() or sen[j][0][0].islower())):
                sen2=[a for (a,b) in sen]    #word extract
                sen3=' '.join(sen2)          #to sentence
                wantsen.append([(sen[i],sen[j]),sen3])
                escape = True
                break
        if escape == True : 
            break
for sen in wantsen[:50]:
    print(sen)
