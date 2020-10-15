import time
from typing import Any, List

from aiohttp.client import ClientSession
from models.slack import SlackHookResponse
from services.slack import EMOJIS, react_to_message, send_message
from services.yelp import yelp_restaurants_to_blocks


async def send_vote_message(
    channel: str, restaurants: List[Any],
):
    blocks = yelp_restaurants_to_blocks(restaurants)
    body = SlackHookResponse(
        **{"text": "Sorry! Couldn't seem to fetch restaurants.", "blocks": blocks}
    )
    async with ClientSession() as session:
        ts = await send_message(session, channel, body)
        for _, emoji in EMOJIS.items():
            await react_to_message(session, channel, emoji, ts)
            time.sleep(0.3)
