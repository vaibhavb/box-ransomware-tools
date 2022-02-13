import os
from boxsdk import OAuth2

def do_Box_OAuth():
    """Box 3-legged OAuth setup"""
    # Dev token is available for 60 mins only, dont use it
    # This script will take hours to run on 500k files, best option is 3-legged OAuth
    OAUTH_KEYS = {
        'BOX_CLIENT_ID':'jzw6abssrlhciah0zaieixlt7ycjaz7b',
        'BOX_CLIENT_SECRET':'Pf13O5cnXLyBGD5G9e8ykwWXtOs3YRYp'
    }
    for key in OAUTH_KEYS.keys():
        if key is None:
            if (os.environ[key]):
                OAUTH_KEYS[key] = os.environ[key]
            else:
                OAUTH_KEYS[key] = input(f'ENTER {key}:')

    oauth = OAuth2(
        client_id=OAUTH_KEYS['BOX_CLIENT_ID'],
        client_secret=OAUTH_KEYS['BOX_CLIENT_SECRET']
    )
    url, _ = oauth.get_authorization_url('http://localhost')
    print('_'*80)
    print(url)
    print('_'*80)
    print("Enter the above URL in the browser and follow the prompts, then copy paste the *CODE* from the last url")
    auth_code=input("Enter the authorization code:")
    access_token, refresh_token = oauth.authenticate(auth_code)
    return oauth