

CLIENT = 'aTl_jFSZylS9aquS0sMSSQ'
SECRET_KEY = 'NMRIrcfCk3RbyCG1Qjga0h6fbgAgKg'

import requests
import pandas as pd

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
headers
res1 = requests.get('https://oauth.reddit.com/r/Bitcoin/hot', headers=headers)


df = pd.DataFrame()
for post in res1.json()['data']['children']:
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title']
    }, ignore_index=True)

print(df)