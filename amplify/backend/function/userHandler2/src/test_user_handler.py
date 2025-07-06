import os
import pytest
import boto3
from moto import mock_dynamodb
# Définit la variable d'environnement AVANT import d'index.py dans la vraie vie
os.environ['STORAGE_USERTABLE2_NAME'] = "user2"
import index



TABLE_NAME = os.environ['STORAGE_USERTABLE2_NAME']

@pytest.fixture
def mock_dynamo_table(monkeypatch):
    with mock_dynamodb():
        # Création de la table mockée
        client = boto3.client('dynamodb', region_name='eu-west-1')
        client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'user_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )

        # Patch la table dans index.py pour utiliser la table mockée
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table(TABLE_NAME)
        monkeypatch.setattr(index, 'table', table)

        yield

def test_add_and_get_user(mock_dynamo_table):
    user_id = 'u001'
    name = 'Alice'
    email = 'alice@example.com'

    index.add_user(user_id, name, email)
    user = index.get_user(user_id)
    assert user is not None
    assert user['user_id'] == user_id
    assert user['name'] == name
    assert user['email'] == email

def test_get_user_not_found(mock_dynamo_table):
    user = index.get_user('does_not_exist')
    assert user is None
