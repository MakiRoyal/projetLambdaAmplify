import boto3
import os
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')


table_name = os.environ['STORAGE_USERTABLE2_NAME']
table = dynamodb.Table(table_name)

def add_user(user_id, name, email):
    response = table.put_item(Item={
        'user_id': user_id,
        'name': name,
        'email': email
    })
    return {"message": f"User {user_id} added successfully."}

def get_user(user_id):
    response = table.get_item(Key={'user_id': user_id})
    return response.get('Item')

def handler(event, context):
    action = event.get('action')
    if action == 'add':
        return add_user(event['user_id'], event['name'], event['email'])
    elif action == 'get':
        return get_user(event['user_id'])
    else:
        return {"error": "Invalid action"}
