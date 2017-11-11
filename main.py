import subprocess
finsen=""
np=list()
pp=list()
vp=list()
#word=input("Enter a word:")
def categorize(word):
    cmd="curl -s \""+"http://api.wordnik.com:80/v4/word.json/"+word+"/definitions?limit=1&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5\" |python3 -mjson.tool | grep partOfSpeech > output.txt"
    print( subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read())
cat=list()
sentence=input("Enter a sentence:")#"Jim begged a book from Mary"
words=sentence.split()
for word in words:
    if word=='a':
        cat.append('article')
    else:
        categorize(word)
        cat.append(open('output.txt', 'r').read())
#print(cat)
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
        i+=1
#print(cat)
    i=0
    while i<len(words):
        print(words[i]+"->"+cat[i])
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
    while len(pp)==0 and len(np)==1 and len(vp)==1 and len(words)==0:
        new=np[0]+" "+vp[0]
        del vp[0]
        del np[0]
        finsen+=new
except:
    pass
print("Noun Phrases:")
print(np)
print("Prep Phrases:")
print(pp)
print("Verb Phrases:")
print(vp)
print("remaining words:")
print(words)
print("Original sentence: "+sentence)
print("Final sentence   : "+finsen)
