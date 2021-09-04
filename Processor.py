# sneeze-translator/Processor.py
from discord import Webhook, RequestsWebhookAdapter, Embed
import re
import discord
import logging
from datetime import datetime
from html import unescape
import random
from translator import request
import os

WH_REGEX = r"discord(app)?\.com\/api\/webhooks\/(?P<id>\d+)\/(?P<token>.+)"
logger = logging.getLogger()


class Processor:
    def __init__(self, status_tweet):
        self.status_tweet = status_tweet
        self.text = ""
        self.url = ""
        self.user = ""
        self.embed = None
        self.footer = os.environ['footer']
        self.initialize()

    def initialize(self):
        logger.info("Initializing Processor")
        if "retweeted_status" in self.status_tweet:
            if "extended_tweet" in self.status_tweet["retweeted_status"]:
                self.text = self.status_tweet["retweeted_status"]["extended_tweet"]["full_text"]
            elif "full_text" in self.status_tweet["retweeted_status"]:
                self.text = self.status_tweet["retweeted_status"]["full_text"]
            else:
                self.text = self.status_tweet["retweeted_status"]["text"]
        elif "extended_tweet" in self.status_tweet:
            self.text = self.status_tweet["extended_tweet"]["full_text"]
        elif "full_text" in self.status_tweet:
            self.text = self.status_tweet["full_text"]
        else:
            self.text = self.status_tweet["text"]

        for url in self.status_tweet["entities"].get("urls", []):
            if url["expanded_url"] is None:
                continue
            self.text = self.text.replace(
                url["url"], "[%s](%s)" % (
                    url["display_url"], url["expanded_url"])
            )
        self.text = unescape(self.text)

        # Unused Hashtag/Mentions hyperlinking
        '''for userMention in self.status_tweet["entities"].get("user_mentions", []):
            self.text = self.text.replace(
                "@%s" % userMention["screen_name"],
                "[@%s](https://twitter.com/%s)"
                % (userMention["screen_name"], userMention["screen_name"]),
            )

        if "extended_tweet" in self.status_tweet:
            for hashtag in sorted(
                self.status_tweet["extended_tweet"]["entities"].get("hashtags", []),
                key=lambda k: k["text"],
                reverse=True,
            ):
                self.text = self.text.replace(
                    "#%s" % hashtag["text"],
                    "[#%s](https://twitter.com/hashtag/%s)" % (hashtag["text"], hashtag["text"]),
                )
        for hashtag in sorted(
            self.status_tweet["entities"].get("hashtags", []),
            key=lambda k: k["text"],
            reverse=True,
        ):
            self.text = self.text.replace(
                "#%s" % hashtag["text"],
                "[#%s](https://twitter.com/hashtag/%s)" % (hashtag["text"], hashtag["text"]),
            )

        self.url = "https://twitter.com/{}/status/{}".format(
            self.status_tweet["user"]["screen_name"], self.status_tweet["id_str"]
        )
        '''

    def attach_field(self):
        logger.info("Attaching fields")
        if "quoted_status" in self.status_tweet:
            if self.status_tweet["quoted_status"].get("text"):
                text = self.status_tweet["quoted_status"]["text"]
                for url in self.status_tweet["quoted_status"]["entities"].get("urls", []):
                    if url["expanded_url"] is None:
                        continue
                    text = text.replace(
                        url["url"], "[%s](%s)" % (
                            url["display_url"], url["expanded_url"])
                    )

                for userMention in self.status_tweet["quoted_status"]["entities"].get(
                    "user_mentions", []
                ):
                    text = text.replace(
                        "@%s" % userMention["screen_name"],
                        "[@%s](https://twitter.com/%s)"
                        % (userMention["screen_name"], userMention["screen_name"]),
                    )

                for hashtag in sorted(
                    self.status_tweet["quoted_status"]["entities"].get(
                        "hashtags", []),
                    key=lambda k: k["text"],
                    reverse=True,
                ):
                    text = text.replace(
                        "#%s" % hashtag["text"],
                        "[#%s](https://twitter.com/hashtag/%s)"
                        % (hashtag["text"], hashtag["text"]),
                    )

                text = unescape(text)
                self.embed.add_field(
                    name=self.status_tweet["quoted_status"]["user"]["screen_name"], value=text
                )

    def attach_media(self):
        logger.info("Attaching media")
        if ("retweeted_status" in self.status_tweet):
            if (
                "extended_tweet" in self.status_tweet["retweeted_status"]
                and "media" in self.status_tweet["retweeted_status"]["extended_tweet"]["entities"]
            ):
                for media in self.status_tweet["retweeted_status"]["extended_tweet"]["entities"][
                    "media"
                ]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass

            if "media" in self.status_tweet["retweeted_status"]["entities"]:
                for media in self.status_tweet["retweeted_status"]["entities"]["media"]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass

            if (
                "extended_entities" in self.status_tweet["retweeted_status"]
                and "media" in self.status_tweet["retweeted_status"]["extended_entities"]
            ):
                for media in self.status_tweet["retweeted_status"]["extended_entities"]["media"]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass
        else:
            if (
                "extended_tweet" in self.status_tweet
                and "media" in self.status_tweet["extended_tweet"]["entities"]
            ):
                for media in self.status_tweet["extended_tweet"]["entities"]["media"]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass

            if "media" in self.status_tweet["entities"]:
                for media in self.status_tweet["entities"]["media"]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass

            if (
                "extended_entities" in self.status_tweet
                and "media" in self.status_tweet["extended_entities"]
            ):
                for media in self.status_tweet["extended_entities"]["media"]:
                    if media["type"] == "photo":
                        self.embed.set_image(url=media["media_url_https"])
                    elif media["type"] == "video":
                        pass
                    elif media["type"] == "animated_gif":
                        pass

    def attach_translation(self):
        translation = request(self.text)
        text_field = "```{}```\n\n*TL: AWS Translate*\n──────────────\n\
            {}\n\n*Original*\n\n".format(translation, self.text) + "{}\n".format(self.footer)
        logger.info(text_field)
        self.embed.description = text_field

    def create_embed(self, color):
        logger.info("Creating embed")
        if "retweeted_status" in self.status_tweet:
            self.user = self.status_tweet["user"]["name"] + " retweeted " + \
                self.status_tweet["retweeted_status"]["user"]["name"]
            thumbnail_url = self.status_tweet["retweeted_status"]["user"]["profile_image_url"]
        else:
            self.user = self.status_tweet["user"]["name"]
            thumbnail_url = self.status_tweet["user"]["profile_image_url"]
        thumbnail_url = thumbnail_url.replace("_normal", "")

        self.embed = Embed(
            url="https://twitter.com/{}/status/{}".format(
                self.status_tweet["user"]["screen_name"], self.status_tweet["id_str"]
            ),
            title=self.user,
            colour=color,
            description=request(self.text),
            timestamp=datetime.strptime(
                self.status_tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y",
            ),


        )

        self.embed.set_thumbnail(url=thumbnail_url)

        self.embed.set_author(
            name=self.status_tweet["user"]["screen_name"],
            url="https://twitter.com/" +
                self.status_tweet["user"]["screen_name"],
            icon_url=self.status_tweet["user"]["profile_image_url"],
        )

    def send_message(self, wh_url):
        logger.info("Sending message")
        match = re.search(WH_REGEX, wh_url)

        if match:
            webhook = Webhook.partial(
                int(match.group("id")), match.group("token"), adapter=RequestsWebhookAdapter()
            )
            try:
                webhook.send(embed=self.embed)
            except discord.errors.NotFound as error:
                logger.info("discord.errors.NotFound - Webhook does not exist")
            except discord.errors.Forbidden as error:
                logger.info(
                    "discord.errors.Forbidden - Authorization token of webhook is incorrect")
            except discord.errors.InvalidArgument as error:
                logger.info("discord.errors.InvalidArgument")
            except discord.errors.HTTPException as error:
                logger.info("discord.errors.HTTPException")
        else:
            logger.info("Webhook URL is invalid.")


if __name__ == "__main__":
    p = Processor()
    p.text = "Kon Kon"
