import streamlit_twitter as st
import pandas as pd
import numpy as np

#Add this otherwise there's an SSL error, think it's Python 3.8
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

st.title("TEM")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://streamlit-project.s3.us-west-1.amazonaws.com/twitter.csv')

