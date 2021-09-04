# sneeze-translator

Discord bot to automatically translate and post a specified Twitter account's tweets to a specified Discord channel.

## Dependencies

* discord.py
* tweepy
* python-dotenv



## Configuration

Create a `.env` file with the following API keys:
* Discord Bot Token
* DeepL API Key
* Twitter Consumer Key
* Twitter Consumer Secret Key
* Twitter Access Token
* Twitter Access Token Secret
* Discord channel Webhook URL 

Edit line 23 of sneeze-translator.py to add the Twitter account ID number of the account you want to target.
```python
USERS = ['0000']
```

You can also edit the `COLOUR` constant in config.py to adjust the colour of the embed posted to the channel.
