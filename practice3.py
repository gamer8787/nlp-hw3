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
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
lm = WordNetLemmatizer()    
# Set of stopwords
stop_words = set(stopwords.words('english'))
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
"""
def is_homograph(word):
    if (not word[1] in accept_list):
        return False
    if (word[0] in stop_words):
        return False
    word=word[0]
    i=0
    URL = "https://en.wiktionary.org/wiki/"+word.lower()
    # print(word) #for debuging
    html = get_html(URL)
    if(html == None):  
        return False
    soup = BeautifulSoup(html, 'html.parser')
    contents1 = soup.find("li",
        {"class": "toclevel-1 tocsection-1"})         
    if contents1 == None :
        return False
    contents = contents1.find_all("li")
    for con in contents:
        c = con.find("a")
        etymology = c["href"]
        if "Etymology" in etymology:
            i=i+1
    if i>1 :
        return True
    else :
        return False
"""
def is_heteronym(word):
    if (not word[1] in accept_list):
        return False
    if (word[0] in stop_words):
        print("stop")
        return False
    word=word[0]
    pro_contents=0 #number of pronunciation contents
    URL = "https://en.wiktionary.org/wiki/"+word.lower()
    html = get_html(URL)
    if(html == None):  
        return False
    soup = BeautifulSoup(html, 'html.parser')

    pronun = soup.find("li",
        {"class": "toclevel-1 tocsection-1"}) 
    pro = pronun.find_all("li")

    for p in pro:
        pp = p.find("a")
        pronunciation = pp["href"]
        if "Pronunciation" in pronunciation:
            pro_contents=pro_contents+1 #number of pronunciation contents

    contain = soup.find("div", {"class" : "mw-parser-output"})
    h3_line=contain.select("h3")
    pro_line_index = pro_contents *[0]
    pro_con=0
    for i,a in enumerate(h3_line):
        if "pronunciation" in a.text.lower():
            pro_line_index[pro_con] = i
            pro_con+=1
        if(pro_con ==pro_contents ):
            break
    #pro_line = contain.select("h3")[pro_line_index]
    #next_pro_line = contain.select("h3")[pro_line_index+1]

    want_tuple=[]
    line_list=[]
    for i in range(pro_contents):
        pro_line = contain.select("h3")[pro_line_index[i]]
        next_pro_line = contain.select("h3")[pro_line_index[i]+1]
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
        if(("IPA(key)" not in line_list[index] and "Rhymes" not in line_list[index] and "UK" not in line_list[index])
                    and "IPA(key)" in line_list[index+1]):
            want_tuple.append([line_list[index], line_list[index+1]])
    print(want_tuple)
    #print(contain.index(pro_line),pro_line.text)
    #print(contain.index(next_pro_line))
    #ul=soup.select("div.mw-parser-output >ul")[2]
    #print(contain.index(ul), ul.text)
    


    return False

def num_homograph(sen):
    i=0
    hetelist=[]
    for word in sen:
        if is_heteronym(word):
            i=i+1
            hetelist.append(word)
    return (i,hetelist)

def tosen(sen):
    sen2=[a for (a,b) in sen]    #word extract
    sen3=' '.join(sen2)
    return sen3
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
print("contrast", is_heteronym(["contrast", "VERB"]))
"""
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
for sen in sentences[:100]:
    senlist.append([num_homograph(sen),tosen(sen)])
senlist.sort(reverse=True) 
print(senlist)"""

#발음이 같으면 