from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
lm = WordNetLemmatizer()    
f = open("CS372_HW2_output_20160638.csv", "w")

brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
brown_editorial_tagged = brown.tagged_words(categories='editorial', tagset='universal')
brown_reviews_tagged = brown.tagged_words(categories='reviews', tagset='universal')
brown_religion_tagged = brown.tagged_words(categories='religion', tagset='universal')
brown_hobbies_tagged = brown.tagged_words(categories='hobbies', tagset='universal')
brown_lore_tagged = brown.tagged_words(categories='lore', tagset='universal')
brown_belles_lettres_tagged = brown.tagged_words(categories='belles_lettres', tagset='universal')
brown_government_tagged = brown.tagged_words(categories='government', tagset='universal')
brown_learned_tagged = brown.tagged_words(categories='learned', tagset='universal')
brown_fiction_tagged = brown.tagged_words(categories='fiction', tagset='universal')
brown_mystery_tagged = brown.tagged_words(categories='mystery', tagset='universal')
brown_science_fiction_tagged = brown.tagged_words(categories='science_fiction', tagset='universal')
brown_adventure_tagged = brown.tagged_words(categories='adventure', tagset='universal')
brown_romance_tagged = brown.tagged_words(categories='romance', tagset='universal')
brown_humor_tagged = brown.tagged_words(categories='humor', tagset='universal')

bigram= [0]*15
bigram[0] = nltk.bigrams(brown_news_tagged)
bigram[1] = nltk.bigrams(brown_editorial_tagged)
bigram[2] = nltk.bigrams(brown_reviews_tagged)
bigram[3] = nltk.bigrams(brown_religion_tagged)
bigram[4] = nltk.bigrams(brown_hobbies_tagged)
bigram[5] = nltk.bigrams(brown_lore_tagged)
bigram[6] = nltk.bigrams(brown_belles_lettres_tagged)
bigram[7] = nltk.bigrams(brown_government_tagged)
bigram[8] = nltk.bigrams(brown_learned_tagged)
bigram[9] = nltk.bigrams(brown_fiction_tagged)
bigram[10] = nltk.bigrams(brown_mystery_tagged)
bigram[11] = nltk.bigrams(brown_science_fiction_tagged)
bigram[12] = nltk.bigrams(brown_adventure_tagged)
bigram[13] = nltk.bigrams(brown_romance_tagged)
bigram[14] = nltk.bigrams(brown_humor_tagged)

text = (brown.words(categories='news') +  brown.words(categories='editorial') + brown.words(categories='reviews')
+ brown.words(categories='religion') + brown.words(categories='hobbies') +  brown.words(categories='lore')
+ brown.words(categories='belles_lettres') + brown.words(categories='government') + brown.words(categories='learned')
+ brown.words(categories='fiction') + brown.words(categories='mystery') + brown.words(categories='science_fiction')
+  brown.words(categories='adventure')+  brown.words(categories='romance') + brown.words(categories='humor'))
imalist = ['very', 'highly', 'extremely', 'completely', 'absolutely', 'rather', 'slightly', 'quite', 'fairly', 'a bit', 'really',
'badly', 'easily'  ] #a few of intensity-modifying adverbs list
a =[] # list of (words in text, its synset.definition)  
for words in text:
    for synset in  wn.synsets(words.lower(), 'a'): # find synset have form adjectve 형용사 it include pos 's'
        for ima in imalist:                # loop for imalsit 
            if ima in synset.definition().split() and len((synset.definition().split())) <=2: # it has simple definition 
                a.append((lm.lemmatize(words.lower(), pos="a"), "ADJ" ,synset.definition())) # (lemmatized words, tag ,its definition)
for words in text:
    for synset in  wn.synsets(words.lower(), 'v'): # find synset have form verb 동사
        for ima in imalist:                #
            if ima in synset.definition().split() and len((synset.definition().split())) <=2: # 
                a.append((lm.lemmatize(words.lower(), pos="v"),"ADV",synset.definition())) # 
for words in text:
    for synset in  wn.synsets(words.lower(), 'n'): # find synset have form verb 명사
        for ima in imalist :           
            if ima in synset.definition().split() and len((synset.definition().split())) <=5: #it has simple definition ex) very good person
                a.append((lm.lemmatize(words.lower(), pos="n"),"NOUN",synset.definition())) # 
b=sorted(set(a)) # sorting it
c=list(b)        # change it to list
modifier = [(a1,a2) for (a1,a2,a3) in c]

accept_list = ["ADJ", "ADV", "NOUN"]
tuple_list = [("ADJ","NOUN"), ("ADV","ADJ"), ("NOUN", "NOUN")]
want_tuple_set=[]
for i in range(15): #we get lemaatize of a0 and b0 and the tag tuple is in the  tuple_list. contain all brown corpus.
    want_tuple_set = want_tuple_set + [((lm.lemmatize(a0),a1),(lm.lemmatize(b0),b1)) for ((a0,a1),(b0,b1)) in bigram[i] 
    if ((a1,b1) in  tuple_list and a0[0].islower() and b0[0].islower() and ((a0,a1) in modifier or (b0,b1) in modifier) )]
print(len(want_tuple_set))
fdist = nltk.FreqDist(want_tuple_set)
print(fdist)
First_count = {} # store counts about first word, first words'tag, second words'tag
for ((a,b),c) in fdist.most_common():
    if (a[0],a[1],b[1]) in First_count :
        First_count[a[0],a[1],b[1]] = First_count[a[0],a[1],b[1]] + c 
    else :
        First_count[a[0],a[1],b[1]] = c
      
fdone=nltk.FreqDist(First_count)

Second_count = {} # store counts about second word, first words'tag, second words'tag
for ((a,b),c) in fdist.most_common():
    if (b[0],a[1],b[1]) in Second_count :
        Second_count[b[0],a[1],b[1]] = Second_count[b[0],a[1],b[1]] + c
      
    else :
        Second_count[b[0],a[1],b[1]] = c
       
fdtwo=nltk.FreqDist(Second_count)

rate_tuple = {} #calculate the frequency and store to it

for ((a,b),c) in fdist.most_common(): 
    rate_tuple[(a[0],b[0],a[1],b[1])] =  [max(c/First_count[a[0],a[1],b[1]],c / Second_count [b[0],a[1],b[1]]), # max(r1,r2), (r1+r2) is measure
    c / First_count[a[0],a[1],b[1]] + c / Second_count [b[0],a[1],b[1]] ,  #another element for viewing
    c / First_count[a[0],a[1],b[1]], c / Second_count [b[0],a[1],b[1]],
    First_count[a[0],a[1],b[1]],Second_count [b[0],a[1],b[1]] ,c]

fdtuple=nltk.FreqDist(rate_tuple)

notevery = [((a,b,c,d),e) for ((a,b,c,d),e) in fdtuple.most_common() if e[6]>=2] #frequency is bigger than 1
print(len(notevery))
print(notevery[:100])
for i in range(100):
        f.write(notevery[i][0][0] + ',' + notevery[i][0][1] + '\n')