import json
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, render_template, request, jsonify   

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("InputOutput.html")    
    
def stemmer(a):
  ps = PorterStemmer() 
  for i in range (0,len(a)):
    stemmed_words=[]
    token=nltk.word_tokenize(a[i])
    #print(token)
    for w in token:
      stemmed_words.append(ps.stem(w))
    t=""
    for k in stemmed_words:
      if(k==stemmed_words[-1]):
        t=t+k
      else:
        t=t+k+" "
    a[i]=t
#print("Filtered Sentence:",filtered_sent)
#stemmer(text1)
#print(text1)
#11

def lemmet(b):
# Init the Wordnet Lemmatizer
  lemmatizer = WordNetLemmatizer()
# Lemmatize list of words and join
#lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
  for i in range (0,len(b)):
    lem_words=[]
    token=nltk.word_tokenize(b[i])
    #print(token)
    for w in token:
      lem_words.append(lemmatizer.lemmatize(w))
    #print(lem_words)
    t=""
    for k in lem_words:
      if(k==lem_words[-1]):
        t=t+k
      else:
        t=t+k+" "
    b[i]=t
#jaccard similiarity
def jaccard_score(x, y):
    """
    Jaccard Similarity J (A,B) = | Intersection (A,B) | /
                                    | Union (A,B) |
    """
    s1 = set(x.split(" "))
    s2 = set(y.split(" "))
    return (len(s1.intersection(s2)) / len(s1.union(s2)))*100

def compare(p,q):
  final=[]
  ntxt1=p.lower()
  ntxt2=q.lower()
# Tokenize: Split the sentence into words
#ntxt1=ntxt1.strip(".")
#,'~','`','!','@','#','$','%','^','&','*','(',')'
# removing punctuation
  ntxt1=ntxt1.replace('!', '').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('_','').replace('-','').replace('+','').replace('=','').replace('[','').replace('{','').replace(']','').replace('}','').replace(';','').replace('|','').replace(':','').replace(',','').replace('<','').replace('>','').replace('/','').replace('?','').replace('`','').replace('~','')
  ntxt1=ntxt1.replace('an','').replace('the','').replace('is','').replace('for','').replace('am','').replace('are','')
  ntxt2=ntxt2.replace('!', '').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('_','').replace('-','').replace('+','').replace('=','').replace('[','').replace('{','').replace(']','').replace('}','').replace(';','').replace('|','').replace(':','').replace(',','').replace('<','').replace('>','').replace('/','').replace('?','').replace('`','').replace('~','')
  ntxt2=ntxt2.replace('an','').replace('the','').replace('is','').replace('for','').replace('am','').replace('are','')
  ntxt1=ntxt1.split(".")
  if ("" in ntxt1):
    ntxt1.remove("")
  ntxt2=ntxt2.split(".")
  if ("" in ntxt2):
    ntxt2.remove("")
  stemmer(ntxt1)
  stemmer(ntxt2)
  lemmet(ntxt1)
  lemmet(ntxt2) 
  less=min(len(ntxt1),len(ntxt2))
  if (less==len(ntxt1)):
    one=ntxt1
    sec=ntxt2
    more=len(ntxt2)
  else:
    one=ntxt2
    sec=ntxt1
    more=len(ntxt1)
  for i in range(0,less):
    final.append([one[i],sec[0]])
    for j in range(0,more):
      
      if jaccard_score(one[i],sec[j])>jaccard_score(final[i][0],final[i][1]):
          final[i][1]=sec[j]
  t=0
  for x in range(0,less):
    t=t+((jaccard_score(final[x][0],final[x][1]))/less)
    
    
  if t>=70.0:
    ans1="<b>You have Plagirized!<br>" 
    ans2="<b>Similiarity percentage= "+str(t)+"</b%<b>"
    return (ans1,ans2)
  else:
    ans1="<b>Did not Plagiarize<br>"
    ans2="<b>Similiarity percentage=<b>"+str(t)+"</b>%<br>"
    return (ans1,ans2)
   
@app.route("/submitJSON", methods=["POST"])



def processJSON(): 
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr) 
    response = ""
    text1=jsonObj['text1']
    text2=jsonObj['text2']
    ans1,ans2=compare(text1,text2)
    response+=ans1
    response+=ans2
  
    
    return response
    
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
