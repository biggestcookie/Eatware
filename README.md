# Eatware

Eatware is a Slackbot that helps you and your team find and vote on nearby places to eat.
Developed for the NCR Hackathon 2020, it uses Dialogflow to receive requests from Slack and process user intents and requirements from natural language.
This repository is the API that Dialogflow makes requests to once parameters are received, and will respond to Slack with a formatted payload using [Slack Blocks](https://api.slack.com/block-kit).

Developed by [@tsyoo](https://github.com/tsyoohub), [@orangegarage](https://github.com/orangegarage), and [@isdoubleac](https://github.com/isdoubleac).

![Slack preview](https://i.imgur.com/BGJhKT2.jpg)

## Requirements

[Python 3.7+](https://www.python.org/downloads/)

Install local development packages using `pip install -r requirements/local.txt`
