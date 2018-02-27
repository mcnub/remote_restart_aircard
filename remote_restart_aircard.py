# Model AirCard 771S

import requests
import requests.utils
import pickle
import time
import re
import hashlib

session = requests.session()
session.cookies.clear()

def get_token():
    global session
    js = session.get('http://192.168.2.1/js/script.js')
    secToken = re.findall('SierraRequest.token =  "(.*)";', js.text)
    if secToken:
        return secToken[0]
    return None

login_page = session.get('http://192.168.2.1/index.html')
if login_page:
    if 'Logout' in login_page.text:
        print('Already logged in')
    else:
        token = get_token()

    
        params = dict()
        
        params['ok_redirect'] = '/index.html'
        params['err_redirect'] = '/index.html'
        params['session.password'] = 'password'
        params['session_password'] = 'password'
        params['remember_password'] = 0
        params['token'] = token
        
        print(params)
        
        process_login = session.post('http://192.168.2.1/Forms/config', params)

        if 'Logout' in process_login.text:
            params = dict()
            params['oma.sprint.start'] = 'PRL'
            params['err_redirect'] = '/error.json'
            params['ok_redirect'] = '/success.json'
            params['token'] = token
            
            post_restart = session.post('http://192.168.2.1/Forms/config', params)
            
            print(post_restart.status_code)
        else:
            print('Failed, Not Logged In')

        