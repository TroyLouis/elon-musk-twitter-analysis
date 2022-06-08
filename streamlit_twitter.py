import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import itertools

# Add this otherwise there's an SSL error, think it's Python 3.8
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Removes a future deprecation warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Global Variables
DATA_URL = ('https://streamlit-project.s3.us-west-1.amazonaws.com/twitter.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def tweets_to_list(data,column_name):
    words = []
    #split tweet into individual words and append to list
    for word in data[column_name]:
        words.append(word.split())
    #turn list of lists into single list
    word_salad = list(itertools.chain(*words))
    #convert list to a string
    word_salad_string = ",".join(word_salad)
    return word_salad_string

def create_word_cloud(wordcloud_words):
    #list of words that won't be included
    stopwords = ['and','it','with','co', 't', 'i', 'https', 'to', 'of','a','that', 'is','the','for','in','if','this']
    wordcloud = WordCloud(stopwords=stopwords).generate(wordcloud_words)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()
    return wordcloud

def create_table(data):
    df = pd.DataFrame(data, columns=['Word','Count'])
    return df

def main():
    st.title("Word Analysis of @elonmusk")
    st.subheader("Word Cloud")

    df_data = load_data(3200)

    tweet_words = tweets_to_list(df_data, 'tweet text')
    wordcloud = create_word_cloud(tweet_words)
    st.write("**Prepositions and some common words have been removed. ")

    word_count = []
    for word in wordcloud.words_.keys():
        word_count.append([word,tweet_words.count(word)])

    table_df = create_table(word_count)
    st.table(table_df)

if __name__ == "__main__":
    main()



