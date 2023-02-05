# importing the required modules
from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as datetime
import streamlit as st

0
st.title("Scrapping Data Using Twitter")

with st.form("Twitter_Scrapping"):
    from_keyword = st.text_input("Enter the tweet")
    number = st.number_input("Enter a number:")
    start = st.date_input("starting date", datetime.date(2020, 1, 1))
    end = st.date_input("end date", datetime.date(2023, 1, 1))
    data = f'"(from:{from_keyword}) since:{start} until:{end}"'
    submitted = st.form_submit_button("Submit")

    list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(data).get_items()):
        if len(list) == number:
            break
        list.append(
            [tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.lang, tweet.source, tweet.likeCount])
    df = pd.DataFrame(list,
                      columns=['Datetime', 'Tweet Id', 'Tweet_url', 'Text', 'Username', 'Reply_count', 'Retweet_count',
                               'Tweet_lang', 'Source', 'Like_count'])
    submit = print(df)
    st.dataframe(df)

# storing data in a database
if st.button("Store  in a data_base"):
    client = MongoClient("mongodb://localhost:27017")
    db = client["twitter_database"]
    new_collection = db["tweet_data"]
    data = df.to_dict(orient='records')
    new_collection.insert_one({"search word": from_keyword, "data": data})


# saving the scrapped data into a csv file
csv = df.to_csv()
st.download_button("Download data as CSV",
                   csv,
                   file_name='tweets_data.csv'
                   )

# saving the scrapped data into a json file
json_file = df.to_json()
st.download_button("Download data as json_file",
                   json_file,
                   file_name='tweets_data.json',
                   )


