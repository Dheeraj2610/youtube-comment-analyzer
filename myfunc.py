#importing necessary libraries
from googleapiclient.discovery import build
import pandas as pd
import re
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

"""
*** fetch comments from youtube
*** @input API builder,video id, empty list
*** @return list of comments
"""
def get_comments(youtube, video_id, comments=[], token=''):
    try:
        video_response = youtube.commentThreads().list(part='snippet',
                                                    videoId=video_id,
                                                    pageToken=token).execute()
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']
            text = comment['snippet']['textDisplay']
            comments.append(text)
        if "nextPageToken" in video_response:
            return get_comments(youtube, video_id, comments, video_response['nextPageToken'])
        else:
            return comments
    except:
        print("error")

"""
*** clean the collected comments 
*** @input video id
*** @output list of cleaned comments(after removing English and Malayalam comments)
"""

def clean_data(video_id):
    try:
        cmts = []
        youtube = build(
            'youtube', 'v3', developerKey='AIzaSyCccTBYCx8YBgOmFlP-j4qQecr1bFWwnRE', cache_discovery=False)
        cmts = get_comments(youtube, video_id,[])
        #removving html tags
        li = []
        pattern = r'<.*?>'
        for i in cmts:
            st = re.sub(pattern, '', i)
            li.append(st)

        #removing malayalam comments
        lis = [w for w in li if re.match(r'[A-Z]+', w, re.I)]
       
        #removing English comments
        words = set(nltk.corpus.words.words())
        lis2 = []
        for i in lis:
            sent = " ".join(w for w in nltk.wordpunct_tokenize(
                i) if w.lower() not in words)  
            lis2.append(sent)
       
        lis3 = [w for w in lis2 if re.match(r'[A-Z]+', w, re.I)]
        return lis3
    except:
        print("error")


"""
*** Predicting the result
*** @input video id
*** @output list of predicted results
"""


def predict_res(link):
    try:
      model = pickle.load(open('svm_model.sav', 'rb')) #load the model
      data = pd.read_csv("Manglish.csv")  #read dataset
      data = data.astype(str) 
      
      X = data["text"]
      Tfidf_Vect = TfidfVectorizer() #Tfidf vectorizer to transform the text into a usable vector
      Tfidf_Vect.fit(X)
      
      cmt = clean_data(link)  #function call to clean the data
      
      if len(cmt) == 0:
        cmt.append("NoComments")
     
      dfr1 = pd.DataFrame(cmt)
      dfr1 = dfr1.iloc[:, 0].str.lower()
      test = Tfidf_Vect.transform(dfr1)  #transform the text into a usable vector
      pred = model.predict(test)  #predicting the result
      return pred
    except:
      print("error")