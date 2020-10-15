import asyncio
import os
import random
import textwrap
from typing import Any, List

from aiohttp import ClientSession
from models.slack import Block, BlockText

from services.slack import EMOJIS

API_BASE_URL = "https://api.yelp.com/v3"
API_SEARCH_URL = f"{API_BASE_URL}/businesses/search"
HEADERS = {"authorization": f"Bearer {os.getenv('yelp_token')}"}
DEFAULT_PARAMS = {
    "limit": 1,
    "price": "1,2",
    "categories": "restaurant",
}


def yelp_restaurants_to_blocks(restaurants: List[Any]) -> List[Block]:
    blocks: List[Block] = []
    for counter, restaurant in enumerate(restaurants):
        rating = round(float(restaurant["rating"]))
        distance_mi = round(float(restaurant["distance"]) * 0.000621371, 1)
        text = f"""\
            :{EMOJIS.get(counter + 1)}: <{restaurant['url']}|*{restaurant['name']}*>
            { "".join([':star:' for _ in range(rating)]) } {restaurant['review_count']} reviews
            { ", ".join([cat['title'] for cat in restaurant['categories']]) }
            { distance_mi } mi - { ", ".join([line for line in restaurant['location']['display_address']]) }
        """
        text = textwrap.dedent(text)
        acc = {
            "image_url": restaurant["image_url"],
            "alt_text": restaurant["name"],
        }
        blocks.append(
            Block(
                **{
                    "type": "section",
                    "text": BlockText(**{"text": text}),
                    "accessory": acc,
                }
            )
        )
    return blocks


async def get_random_restaurants(
    location: str = None,
    radius_m: int = 2500,
    quantity: int = 4,
    search_terms: str = None,
    price: str = None,
) -> List[Any]:
    params = {
        **DEFAULT_PARAMS,
        "location": location or "midtown atlanta",
        "radius": radius_m,
        "term": search_terms,
        "price": price or "1,2",
    }
    async with ClientSession() as session:
        total_results = await __get_total_results(session, params)
        if total_results == 0:
            return []
        return await __get_restaurants_by_random_offset(
            session, total_results, params, quantity
        )


async def __get_restaurants_by_random_offset(
    session: ClientSession, total_restaurants: int, params: Any, quantity: int,
) -> Any:
    tasks = []
    used_offsets = []
    for _ in range(quantity):
        rand_offset: int
        while True:
            rand_offset = random.randint(0, total_restaurants - 2)
            if rand_offset not in used_offsets:
                break
        used_offsets.append(rand_offset)
        tasks.append(__get_single_restaurant(session, rand_offset, params))
    responses = await asyncio.gather(*tasks)
    return responses


async def __get_single_restaurant(
    session: ClientSession, offset: int, params: Any
) -> Any:
    param_offset = {**params, "offset": offset}
    async with session.get(
        API_SEARCH_URL, headers=HEADERS, params=param_offset
    ) as response:
        response_body = await response.json()
        return response_body["businesses"][0]


async def __get_total_results(session: ClientSession, params: Any) -> int:
    total_params = {**params, "offset": 998}
    async with session.get(
        API_SEARCH_URL, headers=HEADERS, params=total_params
    ) as response:
        response_body = await response.json()
        return response_body["total"]
