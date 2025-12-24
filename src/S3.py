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
    return get_user_data_helper(str(user),bucket)
    

