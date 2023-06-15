import requests
import json
from utils import globalapi
import time
import traceback

def getSubs():
    with open ('access_token.txt', 'r') as f:
        token = f.read()
    # Set up variables
    TWITCH_CLIENT_ID = 'your client id'
    TWITCH_OAUTH_TOKEN = token
    USER_NAME = 'your username'

    # Step 1 - Get user ID
    url = f'https://api.twitch.tv/helix/users?login={USER_NAME}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_OAUTH_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    user_data = json.loads(response.text)
    user_id = user_data['data'][0]['id']

    # Step 2 - Get subscriber details
    url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={user_id}&first=100'
    response = requests.get(url, headers=headers)
    sub_data = json.loads(response.text)

    # Step 3 - get all tier 3 subs
    tier3_subs = [sub for sub in sub_data['data'] if sub['tier'] == '3000']
    tier2_subs = [sub for sub in sub_data['data'] if sub['tier'] == '2000']
    subscriber_count_3 = len(tier3_subs)
    subscriber_count_2 = len(tier2_subs)

    # get the next 100 subs
    while 'cursor' in sub_data['pagination']:
        cursor = sub_data['pagination']['cursor']
        url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={user_id}&first=100&after={cursor}'
        response = requests.get(url, headers=headers)
        sub_data = json.loads(response.text)
        tier3_subs.extend([sub for sub in sub_data['data'] if sub['tier'] == '3000'])
        tier2_subs.extend([sub for sub in sub_data['data'] if sub['tier'] == '2000'])
        subscriber_count_3 = len(tier3_subs) - 2
        subscriber_count_2 = len(tier2_subs)

    with open ("subs3.txt", "w+") as s:
        s.write(str(subscriber_count_3))

    with open ("subs2.txt", "w+") as s:
        s.write(str(subscriber_count_2))

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except:
            with open ("refresh_token.txt", "r") as r:
                refresh_token = r.read()
            new_token, new_refresh_token = globalapi.twitch_auth(refresh_token)
            with open ("access_token.txt", "w+") as f:
                f.write(new_token)
            with open ("refresh_token.txt", "w+") as r:
                r.write(new_refresh_token)
            try:
                task()
            except:
                pass
            
        next_time = time.time() + delay

if __name__ == "__main__":
    try:
        getSubs()
    except:
        with open ("refresh_token.txt", "r") as r:
            refresh_token = r.read()
        new_token, new_refresh_token = globalapi.twitch_auth(refresh_token)
        with open ("access_token.txt", "w+") as f:
            f.write(new_token)
        with open ("refresh_token.txt", "w+") as r:
            r.write(new_refresh_token)
        getSubs()
    every(60, getSubs)