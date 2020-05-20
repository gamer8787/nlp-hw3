from nltk.corpus import wordnet as wn
import csv
from nltk.stem import WordNetLemmatizer  
lm = WordNetLemmatizer()                    #it can make word lemma
import nltk
f = open("nlp.csv", "w")
text = nltk.corpus.gutenberg.words('austen-emma.txt')  # I chooese this text, you can change it.
imalist = ['very', 'highly', 'extremely', 'completely', 'absolutely', 'rather', 'slightly', 'quite', 'fairly', 'a bit', 'really'] #a few of intensity-modifying adverbs list
a =[] # list of (words in text, its synset.definition)  
for words in text:
    for synset in  wn.synsets(words, 'a'): # find synset have form adjectve 형용사 it include pos 's'
        for ima in imalist:                # loop for imalsit 
            if ima in synset.definition().split() and len((synset.definition().split())) <=2: # it has simple definition with adverb
                a.append((lm.lemmatize(words, pos="a"),synset.definition())) # (lemmatized words, its definition)
for words in text:
    for synset in  wn.synsets(words, 'v'): # find synset have form verb 동사
        for ima in imalist:                #
            if ima in synset.definition().split() and len((synset.definition().split())) <=2: 
                a.append((lm.lemmatize(words, pos="v"),synset.definition())) # 
b=sorted(set(a)) # sorting it
c=list(b)        # change it to list
#print(c)
#print(len(c))
if (len(c)<50): 
    for i in range(len(c)):
        f.write(c[i][0] + ',' + c[i][1] + '\n')
else :
    for i in range(50):
        f.write(c[i][0] + ',' + c[i][1] + '\n')




    

    