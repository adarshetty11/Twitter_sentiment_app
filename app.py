import streamlit as st
import numpy as np
import pandas as pd 
import plotly.express as ps
from wordcloud import WordCloud , STOPWORDS
import matplotlib.pyplot as plt

st.title('Sentiment Analysis of Tweets about US Airlines')
st.markdown('By Adarsh Shetty')
st.sidebar.title('Sentiment Analysis of Tweets about US Airlines')

st.markdown('This application is a streamlit dashboard to analyse the sentiment of Tweets 🐦')
st.sidebar.markdown('This application is a streamlit dashboard to analyse the sentiment of Tweets 🐦')

data_url = ('Tweets.csv')

#load dataset
@st.cache(persist = True)
def load_data():
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

# display tweet in side bar
st.sidebar.subheader('Show random Tweet')
random_tweet = st.sidebar.radio('Sentiment',('positive','neutral','negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0]) #sample->for selecting random tweet iat-> for displaying just text

#plotting interactive graphs
st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Visualization type',['Histogram','Pie Chart'],key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index , 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox('Hide',True):
    st.markdown('### Number of Tweets by Sentiment')
    if select == 'Histogram':
        fig = ps.bar(sentiment_count,x='Sentiment',y='Tweets',color='Tweets',height=500)
        st.plotly_chart(fig)
    else:
        fig = ps.pie(sentiment_count,names='Sentiment',values='Tweets',color='Tweets',height=500)
        st.plotly_chart(fig)

#plotting interactive map
st.sidebar.subheader('When and where are users tweeeting from?')
hour = st.sidebar.slider('Hour of the day',0,23)
#hour = st.sidebar.number_input('Hour of the day',min_value=1,max_value=24)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox('Close',True):
    st.markdown('### Tweets locations based on the time of the day')
    st.markdown("%i tweets from %i:00 to %i:00" %(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox('Show raw data',False):
        st.write(modified_data)


st.sidebar.subheader('Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick Airlines',(data['airline'].unique()))

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = ps.histogram(choice_data , x='airline' , y='airline_sentiment',histfunc='count',color='airline_sentiment',facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
