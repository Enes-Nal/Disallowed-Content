from botocore.exceptions import ClientError #boto exception
from datetime import datetime
from zoneinfo import ZoneInfo
import json

def get_user_data_helper(user_id : str, bucket):
    key = f'users/{user_id}.json'

    try: 
        user_file = bucket.Object(key) #should cause an exception if user isn't already there
        response = user_file.get()
        data = json.loads(response["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey": #if user key isn't already there:
            #create new user key:
            data = {
                "user_id": user_id,
                "total_violations": 0,
                "word_counts": {},
                "last_updated": None
            }
        else: #otherwise it's an unexpected exception
            raise 
    
    return data


def get_all_users_data_helper(bucket):
    user_files = bucket.objects.filter(Prefix="users/")
    all_data = []
    for user_file in user_files:
        response = user_file.get()
        data = json.loads(response["Body"].read().decode("utf-8"))
        all_data.append(data)
    return all_data


def get_all_users_data_sorted_by_violations_helper(bucket):
    all_data = get_all_user_data_helper(bucket)
    all_data.sort(key=lambda x: x["total_violations"], reverse=True)
    return all_data


def get_all_users_data_sorted_by_word_helper(bucket, word):
    all_data = get_all_user_data_helper(bucket)
    all_data.sort(key=lambda x: x["word_counts"].get(word, 0), reverse=True)
    return all_data


def update_user_data(data, unnallowed_words, words_said):
    for word in words_said:
        if word in unnallowed_words:
            data["word_counts"][word] = data["word_counts"].get(word,0) + 1 # the .get returns the value for [word] if it exists, otherwise returns 0.
            data["total_violations"] += 1

    data["last_updated"] = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %I:%M %p %Z")


def save_user_data(bucket, user_id, data):
    key = f'users/{user_id}.json'
    bucket.Object(key).put(
        Body=json.dumps(data, indent=4),
        ContentType="application/json"
    )