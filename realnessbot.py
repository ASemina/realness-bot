# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 20:16:03 2018

@author: Alexander
"""

#data = '{"text" : "Your message here", "bot_id" : "605ee83200f0482f474a783d6a"}'
#url = "https://api.groupme.com/v3/bots/post"
#response = requests.post('https://api.groupme.com/v3/bots/', data=data)
##response = urllib.request.urlopen(url,data).read().decode()
#print(response)

import requests
import time
import json

last_read = ""
i = 0

with open("auth.json", 'r') as f:
    file = f.readlines()
    auth = json.loads(file[0])

request_params = {'token': auth["token"]}
bot_params = {'text':'','bot_id': auth["bot_id"]}



with open("realness.json", 'r') as f:
    file = f.readlines()
    tallies = json.loads(file[0])


def analyze(message):
    if message['id'] == last_read:
        return True
#    print(message)
    words = message['text'].split()
    for word in words:
        if word.lower() == "holmdell":
            tallies["Victor"] += 5
    
    with open("realness.json", 'w') as f:
        f.write(json.dumps(tallies))
    return False        


while(i < 20):
#    response_post = requests.post('https://api.groupme.com/v3/bots/post', bot_params)
#    if (response_post.headers['Status'] == "202 Accepted"):
       
        response_messages = requests.get('https://api.groupme.com/v3/groups/30589429/messages', params = request_params).json()['response']['messages']
        for message in response_messages:
            check = analyze(message)
            if check:
                break
        message = response_messages[0]
        last_read = message['id']
        
        print(tallies)
        i += 1
        time.sleep(5)


            
    
    
    