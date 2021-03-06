# Eatware

[View our article explanation on this bot, here!](https://medium.com/@biggestcookie/eatware-creation-of-a-flexible-modular-bot-with-dialogflow-and-fastapi-a11b19fa8b25)

Eatware is a Slackbot that helps you and your team find and vote on nearby places to eat.
Developed for the NCR Hackathon 2020, it uses [Dialogflow](https://cloud.google.com/dialogflow) to receive requests from Slack and process user intents and requirements from natural language.
This repository is the API that Dialogflow makes requests to once parameters are received, and will respond to Slack with a formatted payload using [Slack Blocks](https://api.slack.com/block-kit).

Developed by [@tsyoo](https://github.com/tsyoohub), [@orangegarage](https://github.com/orangegarage), [@isdoubleac](https://github.com/isdoubleac), and myself.

![Slack preview](https://i.imgur.com/sY8Y77t.png)


## Requirements

[Python 3.7+](https://www.python.org/downloads/)

Install local development packages using `pip install -r requirements.txt`
