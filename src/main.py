from tradingview_ta import TA_Handler
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy


CLIENT = 'aTl_jFSZylS9aquS0sMSSQ'
SECRET_KEY = 'NMRIrcfCk3RbyCG1Qjga0h6fbgAgKg'
auth = requests.auth.HTTPBasicAuth(CLIENT, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': 'coen424demo',
    'password': '424demo123'
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}


sid = SentimentIntensityAnalyzer()

url="https://cryptopanic.com/api/v1/posts/?auth_token=17d093c57021d47dad85e52ec1ac028d5a980727&kind=news"
auth = tweepy.OAuthHandler("wNZrnH00LuIwJmjihPZfFDOcE", "KwopkAmn5knc0E6Lo8wzeGTPzReaSgaQ1aR4W2cBDdFlGHvzCZ")
auth.set_access_token("1577324299928625154-xuBhQlK4RN3SYSADTinL6NRE4OuFEH",
                      "7qg7YmhutpKKdF0Q2PkgyxWDhK08WgOphf5Hg4Hb2xR3H")

api = tweepy.API(auth)
cryptolist=[["BTCBUSD","r/Bitcoin/hot", 'Bitcoin'], ["ETHBUSD","r/ethtrader/hot", 'Ethereum'],["BNBBUSD","r/bnbchainofficial/hot", 'BNB'], ["XRPBUSD","r/XRP/hot", 'XRP'], ["ADABUSD","r/cardano/hot", 'Cardano'], ["DOGEBUSD","r/dogecoin/hot", 'Dogecoin'],["MATICBUSD","r/polygonnetwork/hot", 'Polygon Matic'],["DOTBUSD","r/Polkadot/hot", 'Polkadot'],["SOLBUSD","r/solana/hot", 'Solana'],["SHIBBUSD","r/shib/hot", 'Shib']]

def calcindex(list):
    for crypto in list:
        print(crypto[2])
        handler = TA_Handler(
            symbol=crypto[0],
            exchange="binance",
            screener="crypto",
            interval="1h",
            timeout=None
        )

        analysis=handler.get_analysis().summary

        buy=(analysis['BUY']/26)*50
        sell=-(analysis['SELL']/26)*50
        indexPrice=buy+sell+50
        print("**********PRICE*************")
        print(indexPrice)


        x=requests.get(url)
        news=x.json()
        newsamount=0
        pos=0
        neg=0
        print("********NEWS*********")
        for article in news["results"]:
            newsamount+=1
            score=sid.polarity_scores(article["title"])
            if score['compound']>0:
                pos+=1
            elif score['compound']<0:
                neg+=1
        indexnews=(((pos/newsamount)*50)-((neg/newsamount)*50))+50
        print(indexnews)


        print("********REDDIT*********")

        redditAPIurl='https://oauth.reddit.com/'+crypto[1]
        res1 = requests.get(redditAPIurl, headers=headers)

        reddittot=0
        redditpos=0
        redditneg=0

        for post in res1.json()['data']['children']:
            reddittot+=1
            nlpscore=sid.polarity_scores(post['data']['title'])
            if nlpscore['compound'] > 0:
                redditpos += 1
            elif nlpscore['compound'] < 0:
                redditneg += 1

        indexreddit=(((redditpos/reddittot)*50)-((redditneg/reddittot)*50))+50
        print(indexreddit)

        crypto_tweets = api.search_tweets(q=crypto[2],lang='en', result_type='top', count = 100)


        print("******************TWITTER**********************")
        tweettot = 0
        tweetpos = 0
        tweetneg = 0
        tweet_list =[]
        for tweet in crypto_tweets:
            text = tweet.text # utf-8 text of tweet
            retweet_count = tweet.retweet_count
            reply_to_user = tweet.in_reply_to_screen_name # if reply original tweetes screenname
            retweets = tweet.retweet_count # number of times this tweet retweeted
            tweet_list.append({'text':text,
                              'retweet_count':retweet_count,
                              'reply_to_user':reply_to_user,
                              'retweets':retweets})
        for btctweet in tweet_list:
            tweettot+=1
            tweetscore=sid.polarity_scores(btctweet['text'])
            if tweetscore['compound'] > 0:
                tweetpos += 1
            elif tweetscore['compound'] < 0:
                tweetneg += 1


        indextwitter = (((tweetpos / tweettot) * 50) - ((tweetneg / tweettot) * 50)) + 50
        print(indextwitter)

        indexsocial=(indextwitter+indexreddit)/2

        cryptoindex=((indexnews/100)*35)+((indexsocial/100)*15)+((indexPrice/100)*50)
        print(cryptoindex)

calcindex(cryptolist)