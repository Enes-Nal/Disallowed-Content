#All functions have been tested
import boto3 #the AWS SDK for Python
from botocore.exceptions import ClientError #boto exception
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from S3_helpers import *

import os
from dotenv import load_dotenv

load_dotenv()
S3_BUCKET = os.getenv('S3_BUCKET')
bucket = boto3.resource('s3').Bucket(S3_BUCKET)


def process_new_message(user : str | int, unnallowed_words : tuple | list, words_said : tuple | list):
    '''
    1. creates new user_file if not already created.
    2. updates counters for disallowed words
    3. updates counter for total violations
    4. saves all the updates back into user file
    '''
    if not user: return # if there's no user then return

    user_id = str(user)

    data = get_user_data_helper(user_id,bucket) #get user data and create user if empty
    update_user_data(data,unnallowed_words,words_said) #updates the data variable counters
    save_user_data(bucket,user_id,data) #saves data back into the S3 bucket
    

def get_user_data(user):
    '''
    data format:
    {
        'user_id' : str(user),
        'total_violations' : int,
        'word_counts' : {
            'word1' : int,
            'word2' : int,
            ...
        },
        'last_updated' : datetime
    }
    '''
    return get_user_data_helper(str(user),bucket)
    
def get_all_user_data():
    '''
    returns a list of all user data
    '''
    return get_all_users_data_helper(bucket)

def get_all_user_data_sorted_by_violations(reverse=True): 
    '''
    returns a list of all user data sorted by total violations
    '''
    return get_all_users_data_sorted_by_violations_helper(bucket, reverse)

def get_all_user_data_sorted_by_word(word, reverse=True):
    '''
    returns a list of all user data sorted by a specific word
    '''
    return get_all_users_data_sorted_by_word_helper(bucket, word, reverse)

def remove_word_from_all_users(word):
    '''
    removes a specific word from all user data
    '''
    all_users = get_all_users_data_helper(bucket)
    for user_data in all_users:
        user_id = user_data['user_id']
        if word in user_data['word_counts']:
            word_count = user_data['word_counts'][word]
            del user_data['word_counts'][word]
            user_data['total_violations'] -= word_count
            save_user_data(bucket,user_id,user_data)

def delete_all_words_from_users():
    '''
    removes all words from all user data
    '''
    all_users = get_all_users_data_helper(bucket)
    for user_data in all_users:
        user_id = user_data['user_id']
        user_data['word_counts'] = {}
        user_data['total_violations'] = 0
        save_user_data(bucket,user_id,user_data)
    