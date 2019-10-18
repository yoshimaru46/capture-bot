from slackbot.bot import respond_to
import re


@respond_to('ping', re.IGNORECASE)
def ping(message):
    message.send('PONG!')
