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

def is_heteronym(word):
    if (not word[1] in accept_list):
        return False
    if (word[0] in stop_words):
        print("stop")
        return False
    word=word[0]
    i=0
    us=0
    uk=0

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
            i=i+1
    if(i>1) :
        return True

    contents = soup.find_all("td",
        {"class": "unicode audiolink"})         
    if contents == None :
        return False
    for con in contents: 
        if "Audio (US)" in str(con):
            us=us+1
        elif "Audio (UK)" in str(con):
            uk=uk+1
    if us+uk>1 :
        return True
    else :
        print(us, uk)
        return False

def num_homograph(sen):
    i=0
    homolist=[]
    for word in sen:
        if is_homograph(word):
            i=i+1
            homolist.append(word)
    return (i,homolist)

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
print("more", is_heteronym(["more", "VERB"]))
for word in wordlist:
    print(word, is_heteronym([word, "VERB"]))
    if(is_heteronym([word, "VERB"])):
        true=true+1
    else:
        false+=1
print(true, false)


"""
sentences = brown.tagged_sents(categories=brown.categories(), tagset='universal')
senlist = []
for sen in sentences[:100]:
    senlist.append([num_homograph(sen),tosen(sen)])
senlist.sort(reverse=True) 
print(senlist)"""
#발음이 같으면 