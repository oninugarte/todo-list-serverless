import logging
import json
import boto3
import os

translate = boto3.client('translate')
dynamodb = boto3.client('dynamodb')
firehose = boto3.client('firehose')

TABLE_NAME = os.getenv('TABLE_NAME')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def translate(event, context):

    logger.info(event)

    if 'source_language' in event and 'target_language' in event and 'review' in event and 'review_id' in event:
        review_id = event['id']
        #source_language = event['source_language']
        target_language = event['language']
        review = event['review']

        try:
            # The Lambda function queries the Amazon DynamoDB table to check whether 
            # the review has already been translated. If the translated review 
            # is already stored in Amazon DynamoDB, the function returns it.
            response = dynamodb.get_item(
                TableName=TABLE_NAME,
                Key={
                    'review_id': {
                        'N': review_id,
                    },
                    'language': {
                        'S': target_language,
                    },
                }
            )
            logger.info(response)
            if 'Item' in response:
                return response['Item']['review']['S']
        except Exception as e:
            logger.error(response)
            raise Exception("[ErrorMessage]: " + str(e))

        try:
            # The Lambda function calls the TranslateText operation and passes the 
            # review, the source language, and the target language to get the 
            # translated review. 
            result = translate.translate_text(Text=review, SourceLanguageCode='auto', TargetLanguageCode=target_language)
            logging.info("Translation output: " + str(result))
        except Exception as e:
            logger.error(response)
            raise Exception("[ErrorMessage]: " + str(e))

        try:
            # After the review is translated, the function stores it using
            # the Amazon DynamoDB putItem operation. Subsequent requests
            # for this translated review are returned from Amazon DynamoDB.
            response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'review_id': {
                    'N': review_id,
                },
                'language': {
                    'S': target_language,
                },
                'review': {
                    'S': result.get('TranslatedText')
                }
                }
            )
            logger.info(response)
        except Exception as e:
                logger.error(e)
                raise Exception("[ErrorMessage]: " + str(e))
        return result.get('TranslatedText')
    else:
        logger.error(e)
        raise Exception("[ErrorMessage]: Invalid input ")
    
