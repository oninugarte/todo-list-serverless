import os
import json

import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def detect_language_task(task):
    response = comprehend.detect_dominant_language(Text='string')
    
    return response

def translate_task(task, source, target):

    response = translate.translate_text(
    Text=task,
    SourceLanguageCode = source,
    TargetLanguageCode = target)
    
    return response


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    target = event['pathParameters']['lang']

    task = result['Item']['text']

    source_result = detect_language_task(task)
    
    source = source_result['Languages'][0]['LanguageCode']
    
    task_translated = translate_task(task, source, target)
    result['Item']['text'] = task_translated['TranslatedText']
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response