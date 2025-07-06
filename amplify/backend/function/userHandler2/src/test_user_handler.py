import os
import pytest
import boto3
from moto import mock_dynamodb
import index  


os.environ['STORAGE_USERTABLE2_NAME'] = "user2"
TABLE_NAME = os.environ['STORAGE_USERTABLE2_NAME']

@pytest.fixture
def mock_dynamo_table(monkeypatch):
    with mock_dynamodb():

        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()


        monkeypatch.setattr(index, 'table', table)

        yield  

def test_add_and_get_user(mock_dynamo_table):
    user_id = 'u001'
    name = 'Alice'
    email = 'alice@example.com'


    response = index.add_user(user_id, name, email)
    assert response['message'] == f"User {user_id} added successfully."


    user = index.get_user(user_id)
    assert user is not None
    assert user['user_id'] == user_id
    assert user['name'] == name
    assert user['email'] == email

def test_get_user_not_found(mock_dynamo_table):
    user = index.get_user('does_not_exist')
    assert user is None
