# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 20:16:03 2018

@author: Alexander
"""

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
def people_load():
    with open("people.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])
##################################################################

#keeps track of the last message checked and i is a 
def last_load():
    with open("last_read.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])["last_read"]
##################################################################

#keeps track of the last message checked
def last_write(last):
    with open("last_read.json", 'w') as f:
        f.write(json.dumps({"last_read":last}))
##################################################################
    
#load group_id
def group_load():
    with open("group.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])["2"]
##################################################################

#secret tokens
def auth_load():
    with open("auth.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])

##################################################################

#the value table
def value_load():
    with open("realness.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])
##################################################################
    
def read(group, request_params):
    response_messages = requests.get('https://api.groupme.com/v3/groups/'+ group +'/messages', params = request_params).json()['response']['messages']
    return response_messages
##################################################################
    
def comment(bot_params):
    response = requests.post('https://api.groupme.com/v3/bots/post', data= bot_params)
##################################################################

def form_comment(person, reason, bot_params):
    if (reason == "realrank"):
        bot_params['text'] = ('The current realness levels are:\n' +
                    'Victor: ' + str(tallies['Victor']) + '\n' +
                    'Alex: ' + str(tallies['Alex']) + '\n' +
                    'Carter: ' + str(tallies['Carter']) + '\n' +
                    'Sean: ' + str(tallies['Sean']) + '\n' +
                    'Sam: ' + str(tallies['Sam']) + '\n' +
                    'Bryan: ' + str(tallies['Bryan']))
        comment(bot_params)
    else:
        bot_params['text'] = 'Not Real. @' + person
        comment(bot_params)
    com = {"Victor":{}, "Alex":{}, "Sean":{}, "Sam":{}, "Carter":{}, "Bryan":{}}
##################################################################
    
#Deal with indivudal people
def anybody(person, word):
    global tallies
    if word in vwords:
        tallies[person] -= 1
    elif word in vwords2:
        tallies[person] += 1
    else:
        return
    form_comment(person, word)
        

def everyone(word):
    global tallies
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

#send the words to specific people        
def analyze(message, last, peep, bot_params):
    if (message['id'] == last):
        return True
    elif message['user_id'] not in peep:
        return False
    elif (str(message['text']).strip() == "Realness Ranking"):
        form_comment("","realrank", bot_params)
    
    person = peep[message['user_id']]
    words = message['text'].split()
    
    for word in words:
        anybody(person, word)
        everyone(word)
    with open("realness.json", 'w') as f:
        f.write(json.dumps(tallies))
    return False        
##################################################################

#Get the messages, finds ones it hasn't read s
def run(last, peep, group, request_params, bot_params):
    global last_read
    i = 0
    while(i < 200):
        response_messages = read(group, request_params)
        for message in response_messages:
            check = analyze(message, last, peep, bot_params)
            if check:
                break
            
        message = response_messages[0]
        last = message['id']
        last_write(last_read)
        i += 1
        time.sleep(1)
##################################################################

if __name__ == "__main__":
    people = people_load()
    last_read = last_load()
    group_id = group_load()
    auth = auth_load()
    tallies = value_load()
    
    request_params = {'token': auth["token"]}
    bot_params = {'text':'','bot_id': auth["bot_id"]}
    
    print('The current realness levels are:\n' \
                'Victor: ' + str(tallies['Victor']) + '\n' \
                'Alex: ' + str(tallies['Alex']) + '\n' \
                'Carter: ' + str(tallies['Carter']) + '\n' \
                'Sean: ' + str(tallies['Sean']) + '\n' \
                'Sam: ' + str(tallies['Sam']) + '\n' \
                'Bryan: ' + str(tallies['Bryan']))
    run(last_read, people, group_id, request_params, bot_params)
    
    
    