# -*- coding: utf-8 -*-
 
#compatibility with Python 3 (so they say...)
from __future__ import print_function

#to get randomness
from random import shuffle

#to make DynamoDB calls
import boto3

#to set timestamps
from datetime import datetime

appName = 'Aikido Kumpel'

#import test, techniques, and graduation techniques
from aikido_techniques import terms, techniques, test_techniques

#helper function to build the speedchlet piece for a DTO for the Alexa interface 
def build_speechlet_response(output, card_text, repromt_text, should_end_session): 
     return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': appName,
            'content': card_text
        },
        'reprompt': {
            'type': 'PlainText',
            'text': repromt_text
        },
        'shouldEndSession': should_end_session
    }
        
#helper function to build DTO to return to the Alexa interface 
def build_response(sessionAttributes, speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': sessionAttributes,
            'response': speechlet_response
        }

#default reply
def default_reply():
    
    output = 'Entschuldige, das kann ich noch nicht...'
    card_text = output
    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                            output, card_text, reprompt_text, should_end_session))

#Welcome message
def welcome_reply():

    #Let's practice in Japanese
    output = "Onagaeschi mass"
    card_text = "Onegaishimasu (DEU: Lass uns zusammen üben)"
    
    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                        output, card_text, reprompt_text, should_end_session))

#Message for stopping or quitting
def leave_reply():

    output = "Dohmo arigatoh"
    card_text = "Domo arigato gozaimasu (DEU: Herzlichsten Dank)"
    
    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = True
    return build_response(sessionAttributes, build_speechlet_response( \
                        output, card_text, reprompt_text, should_end_session))

def help_reply():
    
    output = 'Howdy! Ich helfe dir gerne bei der Vorbereitung für deine naechste Kyu-Pruefung,  \
            indem ich dir zufaellig Techniken aus der Pruefungsordnung fuer den fuenften bis zum ersten Kyu ansage... \
            Am besten sagst du mir gleich, für welchen Kyu du uebst...  \
            Dann frag mich nach einer Technik... \
            Wenn es dir zu schnell geht, wiederhole ich die Technik auch gerne für dich...' 
    card_text = 'Howdy :-) Ich helfe dir gerne bei der Vorbereitung für deine nächste Kyu-Prüfung, '
    card_text += 'indem ich dir zufällig Techniken aus der Prüfungsordnung für den fünften bis zum ersten Kyu ansage. '
    card_text += 'Am besten sagst du mir gleich, für welchen Kyu du übst. '
    card_text += 'Dann frag mich nach einer zufälligen, nächsten Technik. '
    card_text += 'Wenn es dir zu schnell geht, wiederhole ich die Technik auch gerne für dich. '
    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                            output, card_text, reprompt_text, should_end_session))

#get random technique(s)
def random_technique(user, user_tab, number=1):
    
    #set level by user profile
    if 'gradeLevel' in user:
        level = int(user['gradeLevel'])
    else:
        level = 5
    
    #decide whether omote/ura does matter
    omoteUraMode = False
    
    if omoteUraMode:
        tmpEnd = 4    
    else:
        tmpEnd = -1
    
    #make list of random techniques from curriculum
    test_set = range(test_techniques[level-1][0], test_techniques[level-1][1])
    test_length = min(number, len(test_set))
    shuffle(test_set)
    test_set = test_set[0:test_length]
    test_techniques_set = map(techniques.__getitem__, test_set)

    #store last technique
    last_technique = []
    
    #generate output: plain names for card_text and the 'speak' version for voice output
    output = ''
    card_text = ''

    for t in enumerate(test_techniques_set):
        output += ' '.join(map(lambda x: terms[x]['speak'], t[1][:tmpEnd])) + '... '
        card_text += ' '.join(t[1][:tmpEnd]) + '\n '
        print(t[1])
        last_technique = t[1]
    
    try:
        #store last technique in db
        user_tab.update_item(
            Key={
                'userId': user['userId']
            },
            UpdateExpression='set lastTechnique = :t',
            ExpressionAttributeValues={
                ':t': last_technique
            },
            ReturnValues='UPDATED_NEW'
        )
    except:
        print('Database error: Could not update lastTechnique')

    
    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                            output, card_text, reprompt_text, should_end_session))
                            
#repeat last technique
def repeat_technique(user, user_tab):
    output = ''
    card_text = ''

    #decide whether omote/ura does matter
    omoteUraMode = False
    
    if omoteUraMode:
        tmpEnd = 4    
    else:
        tmpEnd = -1
    
    #store last technique in db
    try:
        res = user_tab.get_item(
            Key={
                'userId': user['userId']
            }
        )
    except:
        print('Could not find profile of user ' + user['userId'])
 
    if 'Item' in res and 'lastTechnique' in res['Item']:
        last_technique = res['Item']['lastTechnique'][:tmpEnd]
        print('output: ' + output)
        output = ' '.join(map(lambda x: terms[x]['speak'], last_technique)) + '... '
        card_text = ' '.join(last_technique)
    else:
        last_technique = 'unbekannte Technik'
        output = last_technique
        card_text = lastTechnique

    reprompt_text = 'TODO'
    sessionAttributes = {}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                            output, card_text, reprompt_text, should_end_session))
    
#set kyu grade level you train for
def set_level(intent, user, user_tab):
    
    levelNames = ['ersten', 'zweiten', 'dritten', 'vierten', 'fuenften']
    
    if intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == "ER_SUCCESS_MATCH":
        level = int(intent['slots']['level']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id'])
        user_tab.update_item(
            Key={
                'userId': user['userId']
            },
            UpdateExpression='set gradeLevel = :l',
            ExpressionAttributeValues={
                ':l': level
            },
            ReturnValues='UPDATED_NEW'
        )
        
        
        output = 'Du uebst nun fuer den ' + levelNames[level-1] + ' Kyu.'
        card_text = 'Du übst nun für den ' + levelNames[level-1] + ' Kyu.'
    else:
        output = 'Ich konnte leider nicht verstehen, fuer welchen Kyu du üben möchtest' \
                    'Ich unterstuetze dich vom fünften bis zum ersten Kyu' \
                    'Sag zum Beispiel: Ich möchte für den dritten Kyu üben'
        card_text = 'TODO'

    reprompt_text = 'TODO'
    sessionAttributes = {'level': level}
    should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response( \
                        output, card_text, reprompt_text, should_end_session))
    
#our beloved entry point function
def lambda_handler(event, context):

    print(event)
    
    userId = event['session']['user']['userId']

    ddb = boto3.resource('dynamodb')
    user_tab = ddb.Table('aikido_users')
    
    #try to get userId for existing users
    try:
        user = user_tab.get_item(Key = {'userId': userId})['Item']
        
    #handle request for non-existing users (or in error case: not found users)
    except: 
        
        try:
            user = user_tab.put_item(Item={'userId': userId})
            return help_reply()
    
        #display error
        except:
            print('Database error: Could not add user ' + userId)
  

    #update lastUsed to delete obsolete accounts
    currentTimestamp = datetime.utcnow().isoformat()
    try:
        user_tab.update_item(
            Key={
                'userId': user['userId']
            },
            UpdateExpression='set lastUsed = :t',
            ExpressionAttributeValues={
                ':t': currentTimestamp
                },
            ReturnValues='UPDATED_NEW'
        )
    except:
        print('Database error: Could not update lastUsed')
            
    if event['request']['type'] == "LaunchRequest":
        return welcome_reply()
    elif event['request']['type'] == "IntentRequest":
        if event['request']['intent']['name'] == 'LevelSetzenIntent':
            return set_level(event['request']['intent'], user, user_tab)
        elif event['request']['intent']['name'] == 'TechnikIntent':
            return random_technique(user, user_tab)
        elif event['request']['intent']['name'] == 'AMAZON.RepeatIntent':
            return repeat_technique(user, user_tab)
        elif event['request']['intent']['name'] == 'AMAZON.HelpIntent':
            return help_reply()
        elif event['request']['intent']['name'] == 'AMAZON.StopIntent' \
                or event['request']['intent']['name'] == 'AMAZON.CancelIntent':
            return leave_reply()
        else:
            return default_reply()
    elif event['request']['type'] == "SessionEndRequest":
        return leave_reply()
    else:
        return default_reply()
    
#eof
