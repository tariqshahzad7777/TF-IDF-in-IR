from nltk.stem import WordNetLemmatizer
from nltk import RegexpTokenizer
import contractions
import math
from scipy import spatial

def queryvector(finaldict,querylist,idfscore):       #to generate user queryvector

    queryvect={}
    queryvectlist=[]
    for i in finaldict.keys():
        queryvect[i]=0

    for i in range(len(querylist)):
        wordnet_lemmatizer = WordNetLemmatizer()
        querylist[i] = wordnet_lemmatizer.lemmatize(querylist[i])

    for j in querylist:                      #frequency calculation for each term
        if j in queryvect.keys():
            queryvect[j]=queryvect[j]+1
        else:
            continue

    for j in queryvect.keys():             #query vector generation
        if queryvect[j]==0:
            tf=0
            queryvectlist.append(tf)
        else:
            idf = idfscore[j]
            tf = queryvect[j]
            tfidf = round(tf*idf, 4)
            queryvectlist.append(tfidf)

    return queryvectlist

def preproc():                      #preprocessing word files to get tokenized words

    stoplist=['a','is','the','of','all','and','to','can','be','as','once','for','at','am','are',
             'has','have','had','up','his','her','in','on','no','we','do']

    finaldict={}

    for i in range(1,51):              #traversing through each file
        filename=str(i)+".txt"
        filenum=str(i)
        f=open(filename,"rt",encoding='utf-8')
        document=f.read()
        f.close()

        expanded_words = []

        for word in document.split():          #using contractions to rephrase shortened words
            expanded_words.append(contractions.fix(word))

        text = ' '.join(expanded_words)
        tokenizer = RegexpTokenizer(r"\w+")    #to tokenize and remove all the punctuations

        words = (tokenizer.tokenize(text))
        document = [word.lower() for word in words]

        for i in range(len(document)):          #forming dictionary for TF calculation according to words
            if document[i] in stoplist:
                continue
            else:
                wordnet_lemmatizer = WordNetLemmatizer()
                word=wordnet_lemmatizer.lemmatize(document[i])

                if word in finaldict.keys():
                    if filenum in finaldict[word].keys():
                        finaldict[word][filenum]=finaldict[word][filenum]+1
                    else:
                        finaldict[word][filenum]=1
                else:
                    finaldict[word]={}
                    finaldict[word][filenum]=1

    return finaldict

def createidf(finaldict):                       #creating idf for each document
    idfdict={}
    for i in finaldict.keys():
        listofdocs=len(finaldict[i].keys())
        docfreq=round(math.log(listofdocs,10),4)
        idfdict[i]=round(docfreq/50,4)

    return idfdict

def tfidfgenerator(finaldict,idfscore):           #generating tfidf vector for each document

    docvectors=[]             #contains all the vectors of each document


    for i in range(1,51):
        tempvector=[]                  #tfidf vector for each document
        for j in finaldict.keys():
            if str(i) in finaldict[j].keys():
                idf=idfscore[j]
                tf=finaldict[j][str(i)]
                tfidf=round(tf*idf,4)
                tempvector.append(tfidf)
            else:
                tfidf=0
                tempvector.append(tfidf)
        docvectors.append(tempvector)

    return docvectors

def cosinesimilarity(docvecs,queryvect,userthresh):           #cosine similarity calculation using users alpha value
    resultdict={}

    alpha=round(userthresh,4)
    for i in range(1,51):
        score=1-spatial.distance.cosine(docvecs[i-1],queryvect)          #score calculation
        value=round(score,4)
        if value >= alpha:
            resultdict[value]=i
        else:
            continue

    return resultdict
