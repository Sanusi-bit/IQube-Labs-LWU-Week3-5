#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
import os
import snscrape.modules.twitter as snstweet
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from PIL import Image


# In[28]:


def wordcloud_gen(query):
    stopwords = set(STOPWORDS)
    wc = WordCloud (max_words = 250,stopwords = stopwords,
                   width = 1500, height = 610,
                   min_font_size = 5, max_font_size = 320,
                   background_color = 'white').generate(tweets(query))
    
    image = wc.to_file("wordcloud.png")
    return image
    


# In[29]:


def tweets(query):
    list_of_tweets=[]
    
    tweet_count = 2000
    text_query = query
    since_date = "2020-01-01"
    until_date = "2021-03-31"
    os.system('snscrape --jsonl --max-results {} --since {} twitter-search "{} until:{}"> Jan-ENDSARS-tweets.json'.format(tweet_count, since_date, text_query, until_date))
    scrapped_tweets = pd.read_json('Jan-ENDSARS-tweets.json', lines=True)
    
    list_of_tweets.append(scrapped_tweets['renderedContent'])
    
    df = pd.DataFrame(list_of_tweets, columns=['renderedContent'])
    
    def preprocess_text(text):
        
        #lower case
        text = text.lower()
    
        #replace links with " "
        text = re.sub(r"http\S+", " ", text)

        #replace mentions with " "
        text = re.sub(r"@\S+", " ", text)

        #replace hashtags with " "
        text = re.sub(r"#\S+", " ", text)

        #replacing .com with " "
        text = re.sub(r".com\S+", " ", text)

        #dealing with contractions
        text = re.sub(r"won't\S+", " would not", text)

        #removing space from word
        text = [word.strip() for word in text.split()]

        #removing words less than 2 characters
        text = [word for word in text if len(word)>2]

        #removing twitter amp
        text = [word for word in text if word != 'amp']


        text = ' '.join(text)
        return text
    
    df['renderedContent'] = df['renderedContent'].apply(preprocess_text)
    
    tweets_corpus = ' '.join(tweet for tweet in df['renderedContent'])
    
    return tweets_corpus
    


# In[ ]:




