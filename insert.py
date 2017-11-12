'''
This code checks if the requested word to be categorized exists on the database,if yes,it uses it else it searches for it online and updates the database with the new value and uses the same for further execution
The database name should be NLP, table LIST with attributes word varchar(20) and category varchar(25)
according to the code username is root and password is password, change it accordingly
'''
import MySQLdb
import requests
import json
def categorize(word):
    query = "http://api.wordnik.com:80/v4/word.json/"+word+"/definitions?limit=1&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"
    r = requests.get(query);
    json_data = json.loads(r.text);
    #print("For " + word + " partOfSpeech is " + json_data[0]["partOfSpeech"]);
    return json_data[0]["partOfSpeech"]
db = MySQLdb.connect("localhost","root","password","NLP" )
cursor = db.cursor()
def QUERY(query):
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
        print('error!!\nRolling back changes')
        exit(0)
sentence=input("Enter a sentence:")
words=sentence.split()
for word in words:
    query="select * from LIST where word='%s'"%(word)
    #print(query)
    QUERY(query)
    if(cursor.rowcount==0):
        cat=categorize(word)
        query="insert into LIST values('%s','%s')"%(word,cat)
        QUERY(query)
    else:
        query="select category from LIST where word='%s'"%(word)
        QUERY(query)
        result=cursor.fetchone()
        cat=result[0]
db.close()
