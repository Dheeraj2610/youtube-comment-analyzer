
#importing necessary libraries
from re import S
import streamlit as st
from myfunc import *
import datetime
import googleapiclient.discovery
import plotly.graph_objects as go
import plotly.express as px

x = datetime.datetime.now()

#function to display date and time
def header(content):
    st.markdown(
        f'<p style="background-color:red;color:black;font-size:20px;border-radius:2%;">{content}</p>', unsafe_allow_html=True)


header(x)

DEVELOPER_KEY = "AIzaSyCccTBYCx8YBgOmFlP-j4qQecr1bFWwnRE"  #google api key

#Function to extract comments and analyse
def Extract(keyword,max):
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=DEVELOPER_KEY, cache_discovery=False)
        req = youtube.search().list(q=keyword, part='snippet',
                                    type='video', maxResults=max, pageToken=None)
        res = req.execute()
        ids = []
        for i in res.get("items"):
            try:
                st.write(i.get("snippet").get('title'))  #printing video title
               
                st.write("https://www.youtube.com/watch?v=" +
                        i.get("id").get('videoId'))   #printing video link
                vid = i.get("id").get('videoId') #extracting video id
               
                lis = predict_res(vid)  #predict function call
                
               
                #create a new list by removing neutral comments from the predicted list. considering only positive and negative comments for analysis
                newlist = []
                for i in lis:
                    if i != 'Neutral':
                        newlist.append(i)
               
                #check whether the output list contain minimum 20 results. Analyse when there is more than 20 results      
                if(len(newlist)<20):
                    st.write("Not enough code-mix comments")
                else:
                    freq = {}
                    for item in newlist:
                        if (item in freq):
                            freq[item] += 1
                        else:
                            freq[item] = 1
                    df = pd.DataFrame(columns=['Label', 'Count'])
                    df['Label'] = freq.keys()
                    df['Count'] = freq.values()

                    #plotting pie chart of positive and negative comments
                    fig = go.Figure(go.Pie(
                    labels=df['Label'], values=df['Count'], hoverinfo="label+percent", textinfo="label+value"))  
                    st.header("Analysis")
                    st.plotly_chart(fig)
            except:
                st.write("Comments are disabled for this video")  #in the case of comments disabled videos

st.header("YouTube Video Analyzer")
left, right = st.columns(2)
with left: 
    name = st.text_input("Search Youtube video Here") #textbox to search for a video by keyword
with right:
    max=st.text_input("No.of Videos") #textbox to enter no.of videos to be chosen for analysis
if(st.button('Submit')):
    result = name.title()
    Extract(result,max) #finction call for the analysis
