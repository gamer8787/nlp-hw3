import requests
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer 
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords  
import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
# Set of stopwords
stop_words = set(stopwords.words('english'))
stop_words |= set(['.', ',', '\'s', 'n\'t', '(', ')', "''", "would", "done"]) # refer to the wikitionay 'done' can be a slang also, but except
#f = open("CS372_HW3_output_20160638.csv", "w")
accept_list = ["ADJ", "ADV", "NOUN", "VERB"]
def get_html(url):
    html = ""
    resp = requests.get(url)
    #print(resp)
    if resp.status_code == 200:
        _html = resp.text
    else :
        return None 
    return _html

def is_heteronym(word):
    if (not word[1] in accept_list):
        return (False,None)
    if (word[0] in stop_words):
        #print("stop")
        return (False,None)
    POS = word[1]    
    word=word[0]
    pro_contents=0 #number of pronunciation contents
    URL = "https://en.wiktionary.org/wiki/"+word.lower()
    html = get_html(URL)
    if(html == None):  
        return (False,None)
    soup = BeautifulSoup(html, 'html.parser')
    print(word)
    pronun = soup.find("li",
        {"class": "toclevel-1 tocsection-1"}) 
    if(pronun==None):
        return (False,None)
    pro = pronun.find_all("li")

    for p in pro:
        pp = p.find("a")
        pronunciation = pp["href"]
        if "Pronunciation" in pronunciation:
            pro_contents=pro_contents+1 #number of pronunciation contents
    
    contain = soup.find("div", {"class" : "mw-parser-output"})
    want_tuple=[]
    if(pro_contents == 1):
        h3_line=contain.select("h3")
        pro_line_index = 0
        for i,a in enumerate(h3_line):
            if "pronunciation" in a.text.lower():
                pro_line_index = i
                break
        pro_line = contain.select("h3")[pro_line_index]
        next_pro_line = contain.select("h3")[pro_line_index+1]
        
        want_tuple=[]
        line_list=[]
        for d in contain:
            try:
                index = contain.index(d)
            except:
                continue
            if( contain.index(pro_line) < index < contain.index(next_pro_line)):
                try: 
                    for line in d.text.split("\n"):
                        line_list.append(line)
                except:
                    continue
        #print(line_list)
        for index in range(len(line_list)-1):
            if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "Audio" not in line_list[index]
                and "UK" not in line_list[index] and "US" not in line_list[index])
                        and "IPA(key)" in line_list[index+1]):
                want_tuple.append([line_list[index], IPA(line_list[index+1])])
                #print("1")
                continue
            split=line_list[index].split(" ")
            try:
                a=False
                b=False
                for spl in split:
                    if("IPA(key)" in spl):
                        a=True
                        break
                for spl in split:
                    spl=spl.lower()
                    if("noun" in spl or "adjective" in spl or "verb" in spl or "sense" in spl):
                        pos = spl
                        b=True 
                        break    
                if(a and b):
                    #print("2")
                    want_tuple.append([pos,IPA(line_list[index])])
            except:
                continue
                
        #print(want_tuple)

    if(pro_contents > 1):
        h4_line=contain.select("h4")
        pro_line_index = pro_contents * [0]
        pro_con=0
        for i,a in enumerate(h4_line):
            if "pronunciation" in a.text.lower():
                pro_line_index[pro_con] = i
                pro_con+=1
            if(pro_con ==pro_contents ):
                break
        want_tuple=[]
        line_list=[]
        for i in range(pro_contents):
            pro_line = contain.select("h4")[pro_line_index[i]]
            try:
                next_pro_line = contain.select("h4")[pro_line_index[i]+1] #if no next
                print(next_pro_line.text)
            except:
                for d in contain:
                    try:
                        index = contain.index(d)
                    except:
                        continue
                    if( contain.index(pro_line) <= index):
                        try: 
                            for line in d.text.split("\n"):
                                line_list.append(line)
                        except:
                            continue
            for d in contain:
                try:
                    index = contain.index(d)
                except:
                    continue
                if( contain.index(pro_line) <= index < contain.index(next_pro_line)):
                    try: 
                        for line in d.text.split("\n"):
                            line_list.append(line)
                    except:
                        continue                   
        
            proindex=1
            print("3")
            for index in range(len(line_list)-1):
                if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "Audio" not in line_list[index]
                        and "UK" not in line_list[index] and "US" not in line_list[index] and "Pronunciation" in line_list[index])
                            and "IPA(key)" in line_list[index+1]):
                    want_tuple.append(["pronunciaiton"+str(proindex), IPA(line_list[index+1])])
                    proindex+=1
                    continue
                if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] 
                        and "UK" not in line_list[index] and "US" not in line_list[index])
                            and "IPA(key)" in line_list[index+1]):
                    want_tuple.append([line_list[index], IPA(line_list[index+1])])
                    continue
                try:
                    if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "Audio" not in line_list[index]
                            and "UK" not in line_list[index] and "US" not in line_list[index] and "Pronunciation" in line_list[index])
                                and "IPA(key)" in line_list[index+2]): 
                        want_tuple.append(["pronunciaiton"+str(proindex), IPA(line_list[index+2])])
                        proindex+=1
                except:
                    continue     
        
        if(pro_con !=pro_contents ):
            pro_contents = pro_contents - pro_con
            h3_line=contain.select("h3")
            pro_line_index = pro_contents * [0]
            pro_con=0
            for i,a in enumerate(h3_line):
                if "pronunciation" in a.text.lower():
                    pro_line_index[pro_con] = i
                    pro_con+=1
                if(pro_con ==pro_contents ):
                    break
            #pro_line = contain.select("h3")[pro_line_index]
            #next_pro_line = contain.select("h3")[pro_line_index+1]
            line_list=[]
            for i in range(pro_contents):
                pro_line = contain.select("h3")[pro_line_index[i]]
                next_pro_line = contain.select("h3")[pro_line_index[i]+1]
                for d in contain:
                    try:
                        index = contain.index(d)
                    except:
                        continue
                    if( contain.index(pro_line) <= index < contain.index(next_pro_line)):
                        try: 
                            for line in d.text.split("\n"):
                                line_list.append(line)
                        except:
                            continue
            #print(line_list)
            print("4")                      
            for index in range(len(line_list)-1):
                if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "Audio" not in line_list[index]
                    and "UK" not in line_list[index] and "US" not in line_list[index] and "Pronunciation" in line_list[index])
                            and "IPA(key)" in line_list[index+1]):        
                    want_tuple.append(["pronunciaiton"+str(proindex), IPA(line_list[index+1])])
                    proindex+=1
                    continue
                if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "Audio" not in line_list[index]
                    and "UK" not in line_list[index] and "US" not in line_list[index])
                        and "IPA(key)" in line_list[index+1]):
                    want_tuple.append([line_list[index], IPA(line_list[index+1])])
                    continue
            
    #print((want_tuple))
    if(len(want_tuple)>1):
        a=0
        pronunciation = want_tuple[0][1] #default
        for pos, pronun in want_tuple:
            if POS in pos.upper():
                pronunciation = pronun
                a=1
                break
        if(a==0):
            print("defualt")
        return (True,pronunciation)
        #return (True,want_tuple)
    return (False,None)

def num_heteronym(sen):
    i=0
    hetelist=[]
    for word in sen:
        if is_heteronym(word)[0]:
            i=i+1
            (a,b) = word
            word_and_pronun=(a,b,is_heteronym(word)[1])
            hetelist.append(word_and_pronun)
    return (i,hetelist)

def tosen(sen):
    sen2=[a for (a,b) in sen]    #word extract
    sen3=' '.join(sen2)
    return sen3
def IPA(word):
    if(word.find("/") != -1):
        st=[m.start() for m	in re.finditer('/', word)]
    else:
        st=[word.find("["),word.find("]")]
    return word[st[0]+1:st[1]]

print("abuse", is_heteronym(["abuse", "VERB"]))

#test for real heteronym
"""
URL = "https://en.wiktionary.org/wiki/Category:English_heteronyms"
html = get_html(URL)
soup = BeautifulSoup(html, 'html.parser')

a = soup.find("div", {"class": "mw-category"}) 
b = a.find_all("li") 
wordlist=[]

for k in b:
    c = k.find("a")
    word = c["title"]
    if(word[0].islower() and word not in stop_words):
        wordlist.append(word)

true=0
false=0
for word in wordlist:
    print(word, is_heteronym([word, "VERB"]))
    if(is_heteronym([word, "VERB"])):
        true=true+1
    else:
        false+=1
print(true, false)"""


"""
sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
senlist = []
for i, sen in enumerate(sentences[200:250]):
    senlist.append([num_heteronym(sen),tosen(sen)])
    print(i)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

senlist.sort(reverse=True)
print(senlist) """

#발음이 같으면 