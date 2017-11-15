import subprocess
import requests
import json
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from sys import argv

finsen=""
np=list()
pp=list()
vp=list()

# print(argv)
if len(argv) is 1:
    exit()

db = MySQLdb.connect("localhost","root","password","NLP" )
cursor = db.cursor()
def QUERY(query):
    try:
        cursor.execute(query)
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        db.rollback()
        print('error!!\nRolling back changes')
        exit(0)


def categorize(word):
    query = "select * from list where word = '%s'"%word
    QUERY(query)
    if(cursor.rowcount==0):
        url = "http://api.wordnik.com:80/v4/word.json/"+word+"/definitions?limit=1&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"
        r = requests.get(url);
        # print(word)
        json_data = json.loads(r.text);
        # print("For " + word + " partOfSpeech is " + json_data[0]["partOfSpeech"]);
        query="insert into list values('%s','%s')"%(word,json_data[0]["partOfSpeech"])
        QUERY(query)
        return json_data[0]["partOfSpeech"]; 
    else:
        query="select category from list where word='%s'"%(word)
        QUERY(query)
        result=cursor.fetchone()
        return(result[0])


cat=list()
# sentence=input("Enter a sentence:")#"Jim begged a book from Mary"
sentence = argv[1]
words=sentence.split()
for word in words:
    if word=='a':
        cat.append('article')
    else:
        cat.append(categorize(word))

i=0
try:
    while i<len(cat):
        if "proper-noun" in cat[i]:
            cat[i]='PN'
        if "pronoun" in cat[i]:
            cat[i]='pro'
        if "article" in cat[i]:
            cat[i]='det'
        if "noun" in cat[i]:
            cat[i]='N'
        if "verb" in cat[i]:
            cat[i]='V'
        if "preposition" in cat[i]:
            cat[i]='prep'
        if 'conjunction' in cat[i]:
            cat[i]='conj'
        i+=1
    i=0
    while i<len(words):
        # print(words[i]+"->"+cat[i])
        i+=1
    while 'N' in cat:
        new=words[cat.index('N')]
        del words[cat.index('N')]
        cat.remove('N')
        if 'det' in cat:
            new=words[cat.index('det')]+" "+new
            del words[cat.index('det')]
            cat.remove('det')
        np.append(new)
        new=""
    while 'N' not in cat and 'prep' in cat:
        new=words[cat.index('prep')]+" "+np[0]
        del words[cat.index('prep')]
        cat.remove('prep')
        del np[0]
        pp.append(new)
        new=""
    while 'N' not in cat and 'prep' not in cat and 'V' in cat:
        if(len(np)!=0 and len(pp)!=0):
            new=words[cat.index('V')]+" "+np[0]+" "+pp[0]
            del np[0]
            del words[cat.index('V')]
            cat.remove('V')
            del pp[0]
            vp.append(new)
        elif len(np)!=0 and len(pp)==0:
            new=words[cat.index('V')]+" "+np[0]
            del np[0]
            del words[cat.index('V')]
            cat.remove('V')
            vp.append(new)
        elif len(np)==0 and len(pp)!=0:
            new=words[cat.index('V')]+" "+pp[0]
            del pp[0]
            del words[cat.index('V')]
            cat.remove('V')
            vp.append(new)
        new=""
    while 'N' not in cat and 'prep' not in cat and 'V' not in cat and len(words)==1:
        if(cat[0]=='pro' or cat[0]=='PN'):
            np.append(words[0])
            #finsen=words[0]+" "+vp[0]
            del words[0]
            #del vp[0]
    while len(np)==0 and len(pp)==0 and len(words)>=2 and 'conj' in cat:
        #new=np[0]+" "+words[cat.index('conj')]+" "+np[1]
        new=words[cat.index('PN')]+" "+words[cat.index('conj')]
        del words[cat.index('PN')]
        cat.remove('PN')
        del words[cat.index('conj')]
        cat.remove('conj')
        if 'pro' in cat:
            new=new+" "+words[cat.index('pro')]
            del words[cat.index('pro')]
            cat.remove('pro')
        elif 'PN' in cat:
            new=new+" "+words[cat.index('PN')]
            del words[cat.index('PN')]
            cat.remove('PN')
        np.append(new)
    while len(pp)==0 and len(np)==1 and len(vp)==1 and len(words)==0:
        new=np[0]+" "+vp[0]
        del vp[0]
        del np[0]
        finsen+=new
except:
    pass
# print("Noun Phrases:")
# print(np)
# print("Prep Phrases:")
# print(pp)
# print("Verb Phrases:")
# print(vp)
# print("remaining words:")
# print(words)
# print("Original sentence: "+sentence)
# print("Final sentence   : "+finsen)
print(finsen)
db.close()