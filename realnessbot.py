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


##################################################################

# Bad Words
vwords = []
bwords = []
awords = []
sewords = []
sawords = []
cwords = []
anywords = []
##################################################################

# Good Words
vwords2 = []
bwords2 = []
awords2 = []
sewords2 = []
sawords2 = []
cwords2 = []
anywords2 = []
##################################################################

#load id -> names
with open("people.json", 'r') as f:
    file = f.readlines()
    people = json.loads(file[0])
##################################################################

#keeps track of the last message checked and i is a 
with open("last_read.json", 'r') as f:
    file = f.readlines()
    last_read = json.loads(file[0])["last_read"]
##################################################################

with open("auth.json", 'r') as f:
    file = f.readlines()
    auth = json.loads(file[0])

request_params = {'token': auth["token"]}
bot_params = {'text':'','bot_id': auth["bot_id"]}
##################################################################

with open("realness.json", 'r') as f:
    file = f.readlines()
    tallies = json.loads(file[0])
##################################################################
    
def v(word):
    if word in vwords:
        tallies["Victor"] -= 1
    elif word in vwords2:
        tallies["Victor"] += 1
        
def c(word):
    if word in cwords:
        tallies["Carter"] -= 1
    elif word in cwords2:
        tallies["Carter"] += 1
        
def a(word):
    if word in awords:
        tallies["Alex"] -= 1
    elif word in awords2:
        tallies["Alex"] += 1
        
def se(word):
    if word in sewords:
        tallies["Sean"] -= 1
    elif word in sewords2:
        tallies["Sean"] += 1
        
def sa(word):
    if word in sawords:
        tallies["Sam"] -= 1
    elif word in sawords2:
        tallies["Sam"] += 1
        
def b(word):
    if word in bwords:
        tallies["Bryan"] -= 1
    elif word in bwords2:
        tallies["Bryan"] += 1
        
def anyone(word):
    if word in anywords:
        tallies["Victor"] -= 1
        tallies["Carter"] -= 1
        tallies["Alex"] -= 1
        tallies["Sean"] -= 1
        tallies["Sam"] -= 1
        tallies["Bryan"] -= 1
    elif word in anywords2:
        tallies["Victor"] += 1
        tallies["Carter"] += 1
        tallies["Alex"] += 1
        tallies["Sean"] += 1
        tallies["Sam"] += 1
        tallies["Bryan"] += 1
##################################################################
        
def analyze(message):
    if message['id'] == last_read:
        return True
    words = message['text'].split()
    for word in words:
        v(word)
        c(word)
        se(word)
        sa(word)
        a(word)
        b(word)
        anyone(word)
    with open("realness.json", 'w') as f:
        f.write(json.dumps(tallies))
    return False        
##################################################################

i = 0
while(i < 20):
       
    response_messages = requests.get('https://api.groupme.com/v3/groups/10908178/messages', params = request_params).json()['response']['messages']
    for message in response_messages:
        check = analyze(message)
        if check:
            break
    message = response_messages[0]
    last_read = message['id']
    i += 1
    time.sleep(5)
##################################################################

#keeps track of the last message checked
with open("last_read.json", 'w') as f:
    f.write(json.dumps(file[0]))
##################################################################
    
    
    