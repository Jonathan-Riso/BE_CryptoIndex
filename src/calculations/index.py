from tradingview_ta import TA_Handler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import requests
import tweepy
import datetime
import os

load_dotenv()
CLIENT = os.environ.get('reddit_client')
SECRET_KEY = os.environ.get('reddit_key')
auth = requests.auth.HTTPBasicAuth(CLIENT, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': os.environ.get('reddit_username'),
    'password': os.environ.get('reddit_password')
}

headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}


sid = SentimentIntensityAnalyzer()

url=os.environ.get('crypto_panic_url')
auth = tweepy.OAuthHandler(os.environ.get('tweetpy_key1'), os.environ.get('tweetpy_key2'))
auth.set_access_token(os.environ.get('tweetpy_token1'),
                      os.environ.get('tweetpy_token2'))

api = tweepy.API(auth)
cryptolist={
    "bitcoin": ["BTCBUSD","r/Bitcoin/hot", 'Bitcoin'],
    "ethereum": ["ETHBUSD","r/ethtrader/hot", 'Ethereum'],
    "bnb": ["BNBBUSD","r/bnbchainofficial/hot", 'BNB'],
    "xrp": ["XRPBUSD","r/XRP/hot", 'XRP'],
    "cardano": ["ADABUSD","r/cardano/hot", 'Cardano'],
    "dogecoin": ["DOGEBUSD","r/dogecoin/hot", 'Dogecoin'],
    "polygon matic": ["MATICBUSD","r/polygonnetwork/hot", 'Polygon Matic'],
    "polkadot": ["DOTBUSD","r/Polkadot/hot", 'Polkadot'],
    "solana": ["SOLBUSD","r/solana/hot", 'Solana'],
    "shib": ["SHIBBUSD","r/shib/hot", 'Shib']
}



def calc_index(crypto_name):

    crypto = cryptolist.get(crypto_name)
    if crypto is None:
        raise Exception("Unknown/Not Supported Crypto")

    index_results = {"index": crypto_name}
    
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
    #**********PRICE*************
    index_results["price"] = indexPrice


    x=requests.get(url)
    news=x.json()
    newsamount=0
    pos=0
    neg=0
#    print("********NEWS*********")
    index_results["news"] = {'articles': [], 'score': 0}
    for article in news["results"]:
        newsamount+=1
        title = article["title"]
        index_results["news"]["articles"].append(title) # appending titles for res
        score=sid.polarity_scores(title)
        if score['compound']>0:
            pos+=1
        elif score['compound']<0:
            neg+=1
    indexnews=(((pos/newsamount)*50)-((neg/newsamount)*50))+50
    index_results['news']['score'] = indexnews


#    print("********REDDIT*********")

    redditAPIurl='https://oauth.reddit.com/'+crypto[1]
    res1 = requests.get(redditAPIurl, headers=headers)

    reddittot=0
    redditpos=0
    redditneg=0

    index_results["reddit"] = {'posts': [], 'score': 0}
    for post in res1.json()['data']['children']:
        reddittot+=1
        post_title = post['data']['title']
        index_results["reddit"]["posts"].append(post_title) # appending posts for res
        nlpscore=sid.polarity_scores(post_title)
        if nlpscore['compound'] > 0:
            redditpos += 1
        elif nlpscore['compound'] < 0:
            redditneg += 1

    indexreddit=(((redditpos/reddittot)*50)-((redditneg/reddittot)*50))+50
    index_results['reddit']['score'] = indexreddit

    crypto_tweets = api.search_tweets(q=crypto[2],lang='en', result_type='top', count = 100)


#    print("******************TWITTER**********************")
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
    
    index_results['twitter'] = {}
    index_results['twitter']["tweets"] = tweet_list
    
    for btctweet in tweet_list:
        tweettot+=1
        tweetscore=sid.polarity_scores(btctweet['text'])
        if tweetscore['compound'] > 0:
            tweetpos += 1
        elif tweetscore['compound'] < 0:
            tweetneg += 1


    indextwitter = (((tweetpos / tweettot) * 50) - ((tweetneg / tweettot) * 50)) + 50
    index_results["twitter"]["score"] = indextwitter

    indexsocial=(indextwitter+indexreddit)/2

    cryptoindex=((indexnews/100)*35)+((indexsocial/100)*15)+((indexPrice/100)*50)
    index_results["crypto_index"] = cryptoindex
    index_results["last_updated"] = datetime.datetime.utcnow()

    return index_results
