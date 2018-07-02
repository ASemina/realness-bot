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

#load ids -> names
def people_load():
    with open("people.json", 'r') as f:
        file = f.readlines()
        return json.loads(file[0])
##################################################################
        
#load names -> ids
def people2_load():
    with open("people2.json", 'r') as f:
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
        return json.loads(file[0])["1"]
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

#the value table
def value_write():
    global tallies
    with open("realness.json", 'w') as f:
        f.write(json.dumps(tallies))
##################################################################
    
def read(group, request_params):
    response_messages = requests.get('https://api.groupme.com/v3/groups/'+ group +'/messages', params = request_params).json()['response']['messages']
    return response_messages
##################################################################
    
def comment(bot_params):
    response = requests.post('https://api.groupme.com/v3/bots/post', data= bot_params)
##################################################################

def form_comment(person, reason, bot_params, message=""):
    if (reason == "realrank"):
        bot_params['text'] = ('The current realness levels are:\n' +
                    'Victor: ' + str(tallies['Victor']) + '\n' +
                    'Alex: ' + str(tallies['Alex']) + '\n' +
                    'Carter: ' + str(tallies['Carter']) + '\n' +
                    'Sean: ' + str(tallies['Sean']) + '\n' +
                    'Sam: ' + str(tallies['Sam']) + '\n' +
                    'Bryan: ' + str(tallies['Bryan']))
        comment(bot_params)
    elif (reason == "not"):
        bot_params['text'] = 'Not Real. @' + person
        comment(bot_params)
    elif (reason == "very"):
        bot_params['text'] = 'Very Real. @' + person
        comment(bot_params)
    elif (reason == "nameerror"):
        bot_params['text'] = "I don't recognize that name"
        comment(bot_params)
    elif (reason == "commanderror"):
        bot_params['text'] = "I don't recognize that command"
        comment(bot_params)
    elif (reason == "invalid"):
        bot_params['text'] = "That's not how that works"
        comment(bot_params)
    elif (reason[0] == "help"):
        if (reason[1] == ["notreal"]):
            bot_params['text'] = ("The notreal command is used to shame a user for their lack of realness\n" +
                                  "Example: @db notreal Carter")
        elif (reason[1] == ["veryreal"]):
            bot_params['text'] = ("The veryreal command is used to reward a user for their excess of realness\n" +
                                  "Example: @db veryreal Carter")
        elif (reason[1] == ["Realness", "Ranking"]):
            bot_params['text'] = ("The Realness Ranking command shows how real everyone is\n" +
                                  "Example: @db Realness Ranking")
        else:
            bot_params['text'] = ("These are the following commands:\n" +
                                  "notreal [name]\n" + 
                                  "veryreal [name]\n" +
                                  "Realness Ranking")
        comment(bot_params)
    elif (reason[0] == "all"):
        bot_params['attachments'] = [{'loci': [[0, 1], [2,1], [4,1], [6,1], [8,1], [10,1]], 'type':'mentions', 'user_ids':list(person)}]
        bot_params['text'] = "@everyone " + ' '.join(reason[1])
        comment(bot_params)
#    com = {"Victor":{}, "Alex":{}, "Sean":{}, "Sam":{}, "Carter":{}, "Bryan":{}}
##################################################################
    
#Deal with indivudal people
def anybody(person, word, peep, bot_params):
    if word in vwords:
        minus(person, peep)
    elif word in vwords2:
        add(person, peep)
    else:
        return
    form_comment(person, word, bot_params)        
##################################################################

def everyone(word, peep, bot_params):
    global tallies
    if word in anywords:
        minus("all", peep)
    elif word in anywords2:
        add("all", peep)
##################################################################

def minus(person, peep):
    global tallies
    if (person == "all"):
        for i in peep.values():
            tallies[i] -= 1
    else:
        tallies[person] -= 1
##################################################################
        
def add(person, peep):
    global tallies
    if (person == "all"):
        for i in peep.values():
            tallies[i] += 1
    else:
        tallies[person] += 1
##################################################################

def command(message, peep, people_reverse):
    rest = (str(message['text'][3:]).strip()).lower().split()
    if (len(rest) > 1):
        if (str(message['text'][3:]).lower().strip() == "realness ranking"):     
            return ("", "realrank", True)  
        elif (rest[0] == "notreal"):
            if (rest[1].capitalize() not in peep.values()):
                return ("", "nameerror", True)
            minus(rest[1].capitalize(), peep)
            return(rest[1].capitalize(), "not", True)
        elif (rest[0] == "veryreal"):
            if (rest[1].capitalize() not in peep.values()):
                return ("", "nameerror", True)
            if (message['user_id'] == people_reverse[rest[1].capitalize()]):
                return ("", "invalid", True)
            add(rest[1].capitalize(), peep)    
            return (rest[1].capitalize(), "very", True)
        elif (rest[0] == "help"):
            return ("", ["help", rest[1:]], True)
        elif (rest[0] == "all"):
            p = [*peep]
            return (p, [rest[0], rest[1:]], True)
        else:
            return ("", "commanderror", True)         
    else:
        return ("", ["help", ''], True)
##################################################################

def initial_check(message, last, peep, bot_params, people_reverse):
    if (message['id'] == last):
        return (True, True)
    elif (message['text'] is None):
        return (True, False)
    elif message['user_id'] not in peep:
        return (True, False)
    elif (message['text'][:3] != "@rb"):
        return (False, False)
    else:
        person, reason, truth = command(message, peep, people_reverse)
        form_comment(person, reason, bot_params)
        return (True, False)
##################################################################

#send the words to specific people        
def analyze(message, last, peep, bot_params, people_reverse):
    checkret, checkbreak = initial_check(message, last, peep, bot_params, people_reverse)
    if checkret:
        return checkbreak
    
    person = peep[message['user_id']]
    words = message['text'].split()
    
    for word in words:
        anybody(person, word, peep, bot_params)
        everyone(word, peep, bot_params)
    with open("realness.json", 'w') as f:
        f.write(json.dumps(tallies))
    return False        
##################################################################

#Get the messages, finds ones it hasn't read s
def run(last, peep, group, request_params, bot_params, people_reverse):
    global last_read
    i = 0
    while(i < 20000):
        response_messages = read(group, request_params)
        for message in response_messages:
            check = analyze(message, last, peep, bot_params, people_reverse)
            if check:
                break

        message = response_messages[0]
        last = message['id']
        last_write(last)
        i += 1
        value_write()
        time.sleep(1)
##################################################################

if __name__ == "__main__":
    people = people_load()
    people_reverse = people2_load()
    last_read = last_load()
    group_id = group_load()
    auth = auth_load()
    tallies = value_load()
    
    request_params = {'token': auth["token"]}
    bot_params = {'text':'','bot_id': auth["bot_id"], 'attachments':[]}
    
    print('The current realness levels are:\n' \
                'Victor: ' + str(tallies['Victor']) + '\n' \
                'Alex: ' + str(tallies['Alex']) + '\n' \
                'Carter: ' + str(tallies['Carter']) + '\n' \
                'Sean: ' + str(tallies['Sean']) + '\n' \
                'Sam: ' + str(tallies['Sam']) + '\n' \
                'Bryan: ' + str(tallies['Bryan']))
    run(last_read, people, group_id, request_params, bot_params, people_reverse)
    
    
    