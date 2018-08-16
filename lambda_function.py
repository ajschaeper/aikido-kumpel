# -*- coding: utf-8 -*-
 
#compatibility with Python 3 (so they say...)
from __future__ import print_function

#to get randomness
from random import shuffle

#to make DynamoDB calls
import boto3

#to set timestamps
from datetime import datetime

appName = 'Aikido Köln Prüfungstrainer'

#enable Japanese pronunciation
terms = {
    ### MISC ###
    '': {
        'write': '',
        'speak': ''
    },
    ### STANCES ###
    'suwari waza': {
        'write': 'suwari waza',
        'speak': 'su wari vasa...'
    },
    'hanmi handachi waza': {
        'write': 'hanmi handachi waza',
        'speak': 'hannmi hanndatschi vasa...'
    },
    'tachi waza': {
        'write': 'tachi waza',
        'speak': 'tattschi vasa...'
    },
    ### DIRECTIONS ###
    'omote': {
        'write': 'omote',
        'speak': 'omohte...'
    },
    'ura': {
        'write': 'ura',
        'speak': 'ura...'
    },
    ### ATTACKS ###
    'ai hanmi katate dori': {
        'write': 'aihanmi katate dori',
        'speak': 'aihanmi katate dori...'
    },
    'gyaku hanmi katate dori': {
        'write': 'gyaku hanmi katate dori',
        'speak': 'katate dori...'
    },
    'kata dori': {
        'write': 'kata dori',
        'speak': 'kattah dori...'
    },
    'muna dori': {
        'write': 'muna dori',
        'speak': 'muna dori...'
    },
    'ryote dori': {
        'write': 'ryote dori',
        'speak': 'ryote dori...'
    },
    'katate ryote dori': {
        'write': 'katate ryote dori',
        'speak': 'katate ryote dori...'
    },
    'mae ryo kata dori': {
        'write': 'mae ryo kata dori',
        'speak': 'mae ryo kattah dori...'
    },
    'shomen uchi': {
        'write': 'shomen uchi',
        'speak': 'shomen utschi...'
    },
    'yokomen uchi': {
        'write': 'yokomen uchi',
        'speak': 'yokomen utschi...'
    },
    'kata dori men uchi': {
        'write': 'kata dori men uchi',
        'speak': 'katta dori men utschi...'
    },
    'jodan tsuki': {
        'write': 'jodan tsuki',
        'speak': 'dschodan zki...'
    },
    'chudan tsuki': {
        'write': 'chudan tsuki',
        'speak': 'tschudan zki...'
    },
    'ushiro ryote dori': {
        'write': 'ushiro ryote dori',
        'speak': 'ushiro ryote dori...'
    },
    'ushiro ryo kata dori': {
        'write': 'ushiro ryo kata dori',
        'speak': 'ushiro ryo kattah dori...'
    },
    'ushiro ryo hiji dori': {
        'write': 'ushiro ryo hiji dori',
        'speak': 'ushiro ryo hitschi dori...'
    },
    'ushiro eri dori': {
        'write': 'ushiro eri dori',
        'speak': 'ushiro eri dori...'
    },
    'ushiro katate dori kubi shime': {
        'write': 'ushiro katate dori kubi shime',
        'speak': 'ushiro katatedori kube schime...'
    },
    ### IMMOBILIZATIONS ###
    'ikkyo': {
        'write': 'ikkyo',
        'speak': 'ikkyo'
    },
    'nikyo': {
        'write': 'nikyo',
        'speak': 'nikyo'
    },
    'sankyo': {
        'write': 'sankyo',
        'speak': 'sankyo'
    },
    'yonkyo': {
        'write': 'yonkyo',
        'speak': 'yonkyo'
    },
    'gokyo': {
        'write': 'gokyo',
        'speak': 'gokyo'
    },
    'ude garami': {
        'write': 'ude garami',
        'speak': 'ude garami'
    },
    'hiji kime osae': {
        'write': 'hiji kime osae',
        'speak': 'hitschi kimme ossai'
    },
    ### PROJECTIONS ###
    'kokyu ho': {
        'write': 'kokyu ho',
        'speak': 'kokyu hoo'
    },
    'kokyu nage': {
        'write': 'kokyu nage',
        'speak': 'kokyu nage'
    },
    'irimi nage': {
        'write': 'irimi nage',
        'speak': 'irimi nage'
    },
    'sokumen irimi nage': {
        'write': 'sokumen irimi nage',
        'speak': 'sokumen irimi nage'
    },
    'kote gaeshi': {
        'write': 'kote gaeshi',
        'speak': 'kote geisch'
    },
    'shiho nage': {
        'write': 'shiho nage',
        'speak': 'shiho nage'
    },
    'ude kime nage': {
        'write': 'ude kime nage',
        'speak': 'ude kime nage'
    },
    'tenchi nage': {
        'write': 'tenchi nage',
        'speak': 'tenschi nage'
    },
    'uchi kaiten nage': {
        'write': 'uchi kaiten nage',
        'speak': 'utschikaiten nage'
    },
    'soto kaiten nage': {
        'write': 'soto kaiten nage',
        'speak': 'sotokaiten nage'
    },
    'koshi nage': {
        'write': 'koshi nage',
        'speak': 'koschi nage'
    },
    'juji garami': {
        'write': 'juji garami',
        'speak': 'dschu dschi garami'
    },
    'sumi otoshi': {
        'write': 'sumi otoshi',
        'speak': 'sumi otoshi'
    },
    'aiki otoshi': {
        'write': 'aiki otoshi',
        'speak': 'aiki otoshi'
    },
}

#techniques from fifth to first kyu
techniques = [
    #5 0-10 (11)
    ['suwari waza', 'ryote dori', 'kokyu ho', ''],
    ['tachi waza', 'ai hanmi katate dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ai hanmi katate dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ai hanmi katate dori', 'shiho nage', 'omote'],
    ['tachi waza', 'ai hanmi katate dori', 'shiho nage', 'ura'],
    ['tachi waza', 'ai hanmi katate dori', 'irimi nage', ''],
    ['tachi waza', 'ai hanmi katate dori', 'kote gaeshi', ''],
    ['tachi waza', 'shomen uchi', 'ikkyo', 'omote'],
    ['tachi waza', 'shomen uchi', 'ikkyo', 'ura'],
    ['tachi waza', 'shomen uchi', 'irimi nage', ''],
    ['tachi waza', 'shomen uchi', 'kote gaeshi', ''],
    #4 11-41 (31)
    ['suwari waza', 'ai hanmi katate dori', 'ikkyo', 'omote'],
    ['suwari waza', 'ai hanmi katate dori', 'ikkyo', 'ura'],
    ['suwari waza', 'ai hanmi katate dori', 'irimi nage', ''],    
    ['suwari waza', 'shomen uchi', 'ikkyo', 'omote'],
    ['suwari waza', 'shomen uchi', 'ikkyo', 'ura'],
    ['suwari waza', 'shomen uchi', 'irimi nage', ''], 
    ['tachi waza', 'ai hanmi katate dori', 'nikyo', 'omote'],
    ['tachi waza', 'ai hanmi katate dori', 'nikyo', 'ura'],
    ['tachi waza', 'ai hanmi katate dori', 'ude kime nage', 'omote'],
    ['tachi waza', 'ai hanmi katate dori', 'ude kime nage', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'ikkyo', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'ikkyo', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'nikyo', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'nikyo', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'shiho nage', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'shiho nage', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'kote gaeshi', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'irimi nage', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'sokumen irimi nage', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'uchi kaiten nage', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'uchi kaiten nage', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'ude kime nage', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'ude kime nage', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'tenchi nage', ''],
    ['tachi waza', 'kata dori', 'ikkyo', 'omote'],
    ['tachi waza', 'kata dori', 'ikkyo', 'ura'],
    ['tachi waza', 'kata dori', 'nikyo', 'omote'],
    ['tachi waza', 'kata dori', 'nikyo', 'ura'],
    ['tachi waza', 'ryote dori', 'tenchi nage', ''],
    ['tachi waza', 'shomen uchi', 'nikyo', 'omote'],
    ['tachi waza', 'shomen uchi', 'nikyo', 'ura'],
    #3 43-88 (47)
    ['suwari waza', 'gyaku hanmi katate dori', 'ikkyo', 'omote'],
    ['suwari waza', 'gyaku hanmi katate dori', 'ikkyo', 'ura'],
    ['suwari waza', 'gyaku hanmi katate dori', 'nikyo', 'omote'],
    ['suwari waza', 'gyaku hanmi katate dori', 'nikyo', 'ura'],
    ['suwari waza', 'gyaku hanmi katate dori', 'sankyo', 'omote'],
    ['suwari waza', 'gyaku hanmi katate dori', 'sankyo', 'ura'],
    ['suwari waza', 'gyaku hanmi katate dori', 'irimi nage', ''],    
    ['suwari waza', 'kata dori', 'ikkyo', 'omote'],
    ['suwari waza', 'kata dori', 'ikkyo', 'ura'],
    ['suwari waza', 'kata dori', 'nikyo', 'omote'],
    ['suwari waza', 'kata dori', 'nikyo', 'ura'],
    ['suwari waza', 'kata dori', 'sankyo', 'omote'],
    ['suwari waza', 'kata dori', 'sankyo', 'ura'],
    ['suwari waza', 'shomen uchi', 'nikyo', 'omote'],
    ['suwari waza', 'shomen uchi', 'nikyo', 'ura'],
    ['suwari waza', 'shomen uchi', 'sankyo', 'omote'],
    ['suwari waza', 'shomen uchi', 'sankyo', 'ura'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'shiho nage', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'shiho nage', 'ura'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'uchi kaiten nage', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'uchi kaiten nage', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'sankyo', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'sankyo', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'ude garami', ''],
    ['tachi waza', 'kata dori', 'sankyo', 'omote'],
    ['tachi waza', 'kata dori', 'sankyo', 'ura'],
    ['tachi waza', 'ryote dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ryote dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ryote dori', 'shiho nage', 'omote'],
    ['tachi waza', 'ryote dori', 'shiho nage', 'ura'],
    ['tachi waza', 'ryote dori', 'irimi nage', ''],
    ['tachi waza', 'shomen uchi', 'sankyo', 'omote'],
    ['tachi waza', 'shomen uchi', 'sankyo', 'ura'],
    ['tachi waza', 'yokomen uchi', 'kote gaeshi', ''],
    ['tachi waza', 'yokomen uchi', 'shiho nage', 'omote'],
    ['tachi waza', 'yokomen uchi', 'shiho nage', 'ura'],
    ['tachi waza', 'yokomen uchi', 'irimi nage', ''],
    ['tachi waza', 'yokomen uchi', 'ude kime nage', 'omote'],
    ['tachi waza', 'yokomen uchi', 'ude kime nage', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'nikyo', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'nikyo', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'sankyo', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'sankyo', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'kote gaeshi', ''],
    ['tachi waza', 'ushiro ryote dori', 'kokyu nage', ''],
    #2 89-162 (74) 
    ['suwari waza', 'gyaku hanmi katate dori', 'yonkyo', 'omote'],
    ['suwari waza', 'gyaku hanmi katate dori', 'yonkyo', 'ura'],
    ['suwari waza', 'shomen uchi', 'yonkyo', 'omote'],
    ['suwari waza', 'shomen uchi', 'yonkyo', 'ura'],
    ['suwari waza', 'yokomen uchi', 'ikkyo', 'omote'],
    ['suwari waza', 'yokomen uchi', 'ikkyo', 'ura'],
    ['suwari waza', 'yokomen uchi', 'nikyo', 'omote'],
    ['suwari waza', 'yokomen uchi', 'nikyo', 'ura'],
    ['suwari waza', 'yokomen uchi', 'sankyo', 'omote'],
    ['suwari waza', 'yokomen uchi', 'sankyo', 'ura'],
    ['suwari waza', 'yokomen uchi', 'irimi nage', ''],    
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'kote gaeshi', ''],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'soto kaiten nage', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'soto kaiten nage', 'ura'],
    ['hanmi handachi waza', 'ryote dori', 'shiho nage', 'omote'],
    ['hanmi handachi waza', 'ryote dori', 'shiho nage', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'soto kaiten nage', 'omote'],
    ['hanmi handachi waza', 'shomen uchi', 'soto kaiten nage', 'ura'],
    ['tachi waza', 'ai hanmi katate dori', 'koshi nage', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'yonkyo', 'omote'],
    ['tachi waza', 'gyaku hanmi katate dori', 'yonkyo', 'ura'],
    ['tachi waza', 'gyaku hanmi katate dori', 'koshi nage', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'kokyu nage', ''],
    ['tachi waza', 'ryote dori', 'kote gaeshi', ''],
    ['tachi waza', 'ryote dori', 'ude kime nage', 'omote'],
    ['tachi waza', 'ryote dori', 'ude kime nage', 'ura'],
    ['tachi waza', 'katate ryote dori', 'ikkyo', 'omote'],
    ['tachi waza', 'katate ryote dori', 'ikkyo', 'ura'],
    ['tachi waza', 'katate ryote dori', 'nikyo', 'omote'],
    ['tachi waza', 'katate ryote dori', 'nikyo', 'ura'],
    ['tachi waza', 'katate ryote dori', 'sankyo', 'omote'],
    ['tachi waza', 'katate ryote dori', 'sankyo', 'ura'],
    ['tachi waza', 'katate ryote dori', 'yonkyo', 'omote'],
    ['tachi waza', 'katate ryote dori', 'yonkyo', 'ura'],
    ['tachi waza', 'katate ryote dori', 'shiho nage', 'omote'],
    ['tachi waza', 'katate ryote dori', 'shiho nage', 'ura'],
    ['tachi waza', 'katate ryote dori', 'kote gaeshi', ''],
    ['tachi waza', 'katate ryote dori', 'irimi nage', ''],
    ['tachi waza', 'katate ryote dori', 'kokyu nage', ''],
    ['tachi waza', 'kata dori men uchi', 'ikkyo', 'omote'],
    ['tachi waza', 'kata dori men uchi', 'ikkyo', 'ura'],
    ['tachi waza', 'kata dori men uchi', 'nikyo', 'omote'],
    ['tachi waza', 'kata dori men uchi', 'nikyo', 'ura'],
    ['tachi waza', 'kata dori men uchi', 'sankyo', 'omote'],
    ['tachi waza', 'kata dori men uchi', 'sankyo', 'ura'],
    ['tachi waza', 'kata dori men uchi', 'yonkyo', 'omote'],
    ['tachi waza', 'kata dori men uchi', 'yonkyo', 'ura'],
    ['tachi waza', 'kata dori men uchi', 'shiho nage', ''],
    ['tachi waza', 'kata dori men uchi', 'kote gaeshi', ''],
    ['tachi waza', 'kata dori men uchi', 'irimi nage', ''],
    ['tachi waza', 'kata dori men uchi', 'kokyu nage', ''],
    ['tachi waza', 'shomen uchi', 'yonkyo', 'omote'],
    ['tachi waza', 'shomen uchi', 'yonkyo', 'ura'],
    ['tachi waza', 'shomen uchi', 'shiho nage', 'omote'],
    ['tachi waza', 'shomen uchi', 'shiho nage', 'ura'],
    ['tachi waza', 'shomen uchi', 'soto kaiten nage', 'omote'],
    ['tachi waza', 'shomen uchi', 'soto kaiten nage', 'ura'],
    ['tachi waza', 'yokomen uchi', 'ikkyo', 'omote'],
    ['tachi waza', 'yokomen uchi', 'ikkyo', 'ura'],
    ['tachi waza', 'yokomen uchi', 'nikyo', 'omote'],
    ['tachi waza', 'yokomen uchi', 'nikyo', 'ura'],
    ['tachi waza', 'yokomen uchi', 'sankyo', 'omote'],
    ['tachi waza', 'yokomen uchi', 'sankyo', 'ura'],
    ['tachi waza', 'yokomen uchi', 'yonkyo', 'omote'],
    ['tachi waza', 'yokomen uchi', 'yonkyo', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'yonkyo', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'yonkyo', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'irimi nage', ''],
    ['tachi waza', 'ushiro ryote dori', 'ude kime nage', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'ude kime nage', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'shiho nage', 'omote'],
    ['tachi waza', 'ushiro ryote dori', 'shiho nage', 'ura'],
    ['tachi waza', 'ushiro ryo kata dori', 'sokumen irimi nage', ''],
    ['tachi waza', 'ushiro ryo kata dori', 'kokyu nage', ''],
    #1 163-254 (92)
    ['suwari waza', 'shomen uchi', 'gokyo', ''],
    ['suwari waza', 'yokomen uchi', 'gokyo', ''],
    ['suwari waza', 'yokomen uchi', 'kote gaeshi', ''],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'ikkyo', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'ikkyo', 'ura'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'nikyo', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'nikyo', 'ura'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'sankyo', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'sankyo', 'ura'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'yonkyo', 'omote'],
    ['hanmi handachi waza', 'gyaku hanmi katate dori', 'yonkyo', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'ikkyo', 'omote'],
    ['hanmi handachi waza', 'shomen uchi', 'ikkyo', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'nikyo', 'omote'],
    ['hanmi handachi waza', 'shomen uchi', 'nikyo', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'sankyo', 'omote'],
    ['hanmi handachi waza', 'shomen uchi', 'sankyo', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'yonkyo', 'omote'],
    ['hanmi handachi waza', 'shomen uchi', 'yonkyo', 'ura'],
    ['hanmi handachi waza', 'shomen uchi', 'irimi nage', ''],
    ['hanmi handachi waza', 'shomen uchi', 'kote gaeshi', ''],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'ikkyo', 'omote'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'ikkyo', 'ura'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'nikyo', 'omote'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'nikyo', 'ura'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'sankyo', 'omote'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'sankyo', 'ura'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'yonkyo', 'omote'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'yonkyo', 'ura'],
    ['hanmi handachi waza', 'ushiro ryo kata dori', 'kokyu nage', ''],
    ['tachi waza', 'gyaku hanmi katate dori', 'sumi otoshi', ''],
    ['tachi waza', 'mae ryo kata dori', 'kokyu nage', ''],
    ['tachi waza', 'muna dori', 'shiho nage', 'omote'],
    ['tachi waza', 'muna dori', 'shiho nage', 'ura'],
    ['tachi waza', 'katate ryote dori', 'juji garami', ''],
    ['tachi waza', 'shomen uchi', 'gokyo', ''],
    ['tachi waza', 'shomen uchi', 'kokyu nage', ''],
    ['tachi waza', 'shomen uchi', 'koshi nage', ''],
    ['tachi waza', 'yokomen uchi', 'gokyo', ''],
    ['tachi waza', 'yokomen uchi', 'kokyu nage', ''],
    ['tachi waza', 'yokomen uchi', 'koshi nage', ''],
    ['tachi waza', 'jodan tsuki', 'ikkyo', 'omote'],
    ['tachi waza', 'jodan tsuki', 'ikkyo', 'ura'],
    ['tachi waza', 'jodan tsuki', 'nikyo', 'omote'],
    ['tachi waza', 'jodan tsuki', 'nikyo', 'ura'],
    ['tachi waza', 'jodan tsuki', 'sankyo', 'omote'],
    ['tachi waza', 'jodan tsuki', 'sankyo', 'ura'],
    ['tachi waza', 'jodan tsuki', 'yonkyo', 'omote'],
    ['tachi waza', 'jodan tsuki', 'yonkyo', 'ura'],
    ['tachi waza', 'jodan tsuki', 'shiho nage', 'omote'],
    ['tachi waza', 'jodan tsuki', 'shiho nage', 'ura'],
    ['tachi waza', 'jodan tsuki', 'irimi nage', ''],
    ['tachi waza', 'jodan tsuki', 'hiji kime osae', ''],
    ['tachi waza', 'chudan tsuki', 'ikkyo', 'omote'],
    ['tachi waza', 'chudan tsuki', 'ikkyo', 'ura'],
    ['tachi waza', 'chudan tsuki', 'nikyo', 'omote'],
    ['tachi waza', 'chudan tsuki', 'nikyo', 'ura'],
    ['tachi waza', 'chudan tsuki', 'sankyo', 'omote'],
    ['tachi waza', 'chudan tsuki', 'sankyo', 'ura'],
    ['tachi waza', 'chudan tsuki', 'yonkyo', 'omote'],
    ['tachi waza', 'chudan tsuki', 'yonkyo', 'ura'],
    ['tachi waza', 'chudan tsuki', 'irimi nage', ''],
    ['tachi waza', 'chudan tsuki', 'kote gaeshi', ''],
    ['tachi waza', 'chudan tsuki', 'soto kaiten nage', 'omote'],
    ['tachi waza', 'chudan tsuki', 'soto kaiten nage', 'ura'],
    ['tachi waza', 'chudan tsuki', 'uchi kaiten nage', 'omote'],
    ['tachi waza', 'chudan tsuki', 'uchi kaiten nage', 'ura'],
    ['tachi waza', 'ushiro ryote dori', 'sokumen irimi nage', ''],
    ['tachi waza', 'ushiro ryote dori', 'juji garami', ''],
    ['tachi waza', 'ushiro ryote dori', 'koshi nage', ''],
    ['tachi waza', 'ushiro ryo kata dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ushiro ryo kata dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ushiro ryo kata dori', 'nikyo', 'omote'],
    ['tachi waza', 'ushiro ryo kata dori', 'nikyo', 'ura'],
    ['tachi waza', 'ushiro ryo kata dori', 'sankyo', 'omote'],
    ['tachi waza', 'ushiro ryo kata dori', 'sankyo', 'ura'],
    ['tachi waza', 'ushiro ryo kata dori', 'yonkyo', 'omote'],
    ['tachi waza', 'ushiro ryo kata dori', 'yonkyo', 'ura'],
    ['tachi waza', 'ushiro ryo kata dori', 'aiki otoshi', ''],
    ['tachi waza', 'ushiro ryo hiji dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ushiro ryo hiji dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ushiro ryo hiji dori', 'kokyu nage', ''],
    ['tachi waza', 'ushiro eri dori', 'ikkyo', 'omote'],
    ['tachi waza', 'ushiro eri dori', 'ikkyo', 'ura'],
    ['tachi waza', 'ushiro eri dori', 'kote gaeshi', ''],
    ['tachi waza', 'ushiro eri dori', 'shiho nage', 'omote'],
    ['tachi waza', 'ushiro eri dori', 'shiho nage', 'ura'],
    ['tachi waza', 'ushiro katate dori kubi shime', 'ikkyo', 'omote'],
    ['tachi waza', 'ushiro katate dori kubi shime', 'ikkyo', 'ura'],
    ['tachi waza', 'ushiro katate dori kubi shime', 'kote gaeshi', ''],
    ['tachi waza', 'ushiro katate dori kubi shime', 'shiho nage', 'omote'],
    ['tachi waza', 'ushiro katate dori kubi shime', 'shiho nage', 'ura']
]

#indices in techniques arrays that indicate the part of the syllabus for a repective kyu
test_techniques = [
    [163,255],
    [89,163],
    [42,89],
    [11,42],
    [0, 11]
]

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
