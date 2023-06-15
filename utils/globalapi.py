from twitchio.ext import commands, routines
import requests
import requests_cache
import datetime
import os
from twitchAPI.oauth import refresh_access_token
import asyncio

async def twitch_auth_func(refresh_token):
    client_id = 'your client id'
    client_secret = 'your client secret'
    new_token, new_refresh_token = await refresh_access_token(refresh_token, client_id, client_secret)
    return new_token, new_refresh_token

def twitch_auth(refresh_token):
    return asyncio.run(twitch_auth_func(refresh_token))
    

if __name__ == "__main__":
    print(twitch_auth('your refresh token'))