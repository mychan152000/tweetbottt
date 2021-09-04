from typing import Text
import requests
import json
import urllib.parse
from dotenv import load_dotenv
import os
import logging
import boto3

# load_dotenv()
# API_ENDPOINT = 'https://api-free.deepl.com/v2/translate'
# DEEPL_KEY = os.getenv('DEEPL_KEY')
logger = logging.getLogger()
translate = boto3.client(service_name='translate',
                         region_name='us-east-1',
                         use_ssl=True,
                         aws_access_key_id=os.environ['aws_access_key_id'],
                         aws_secret_access_key=os.environ['aws_secret_access_key'],
                         )


def request(message):
    # query = {'auth_key': DEEPL_KEY,
    #     'text': message,
    #     'source_lang': 'JA',
    #     'target_lang': 'EN-GB',
    #     'split_sentences': '1',
    #     'preserve_formatting': '1',
    #     'formality': 'default'}
    result = translate.translate_text(Text=message,
                                      SourceLanguageCode="ja",
                                      TargetLanguageCode="en")
    try:
        # response = requests.get(params=result).json()
        logger.info(result)
        text = result.get('TranslatedText')
        logger.info(text)
        return text
    except requests.ConnectionError as errc:
        logger.info(errc)
    except requests.exceptions.HTTPError as errh:
        logger.info(errh)
    except requests.Timeout as errt:
        logger.info(errt)
    except requests.RequestException as err:
        logger.info(err)
