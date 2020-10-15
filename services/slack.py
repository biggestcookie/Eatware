import os
from typing import Dict

from aiohttp import ClientSession, FormData
from fastapi.encoders import jsonable_encoder

from models.slack import SlackHookResponse, SlackMessageBody

BOT_USER_ID = "U018156PVJQ"
CHANNEL = "C0187HP77EV"

API_BASE_URL = "https://slack.com/api"
API_CONVERSATION_HISTORY_URL = f"{API_BASE_URL}/conversations.history?channel={CHANNEL}"
API_ADD_REACT_URL = f"{API_BASE_URL}/reactions.add"
API_GET_REACT_URL = f"{API_BASE_URL}/reactions.get"
API_SEND_MSG_URL = f"{API_BASE_URL}/chat.postMessage"
TOKEN = os.getenv("slack_token")
HEADERS = {"authorization": f"Bearer {TOKEN}"}
DEFAULT_PARAMS = {"token": TOKEN}


async def get_last_bot_message(session: ClientSession):
    async with session.get(API_CONVERSATION_HISTORY_URL, headers=HEADERS) as response:
        response_body = await response.json()
        for msg in response_body:
            if msg["user"] == BOT_USER_ID:
                return msg["ts"]


async def react_to_message(session: ClientSession, channel: str, name: str, ts: str):
    async with session.post(
        API_ADD_REACT_URL,
        headers=HEADERS,
        data=FormData(
            {**DEFAULT_PARAMS, "channel": channel, "name": name, "timestamp": ts}
        ),
    ) as response:
        response_body = await response.json()
        print(response_body)


async def tally_reactions(session: ClientSession, channel: str, ts: str) -> Dict:
    react_dict = {"one": 0, "two": 0, "three": 0, "four": 0}

    async with session.get(
        API_GET_REACT_URL,
        headers=HEADERS,
        params={**DEFAULT_PARAMS, "channel": channel, "timestamp": ts},
    ) as response:
        response_body = await response.json()
        reactions = response_body["message"]["reactions"]
        for reaction in reactions:
            if reaction["name"] in react_dict:
                react_dict[reaction["name"]] = reaction["count"] - 1
        return react_dict


async def send_message(
    session: ClientSession, channel: str, body: SlackHookResponse
) -> str:
    message_body = SlackMessageBody(
        **{
            **DEFAULT_PARAMS,
            "text": body.text,
            "blocks": body.blocks,
            "channel": channel,
        }
    )
    async with session.post(
        API_SEND_MSG_URL, headers=HEADERS, json=jsonable_encoder(message_body),
    ) as response:
        response_body = await response.json()
        return response_body["ts"]


def get_restaurant_names(msg) -> Dict:
    names = {":one:": "", ":two:": "", ":three:": "", ":four:": ""}
    blocks = msg["messages"][0]["blocks"]
    for block in blocks:
        text = block["text"]["text"]
        for key in names:
            if key in text:
                names[key] = text[text.index("*") + 1: text.index(":star:") - 3]
    return names


def process_voting_results(voting_results: Dict) -> Dict:
    win = {"max": 0}
    for key in voting_results:
        if voting_results[key] == win["max"]:
            win[key] = voting_results[key]
        if voting_results[key] > win["max"]:
            win = {"max": voting_results[key]}
    return win
