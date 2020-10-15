import json
from typing import Optional

from fastapi import APIRouter, Request

from models.slack import SlackHookResponse
from services import yelp
from services.yelp import yelp_restaurants_to_blocks

router = APIRouter()


@router.post("")
async def post(request: Request) -> SlackHookResponse:
    body = await request.form()
    print(json.dumps(dict(body), indent=4, sort_keys=True))

    args = body.get("text").split(",")
    location: str
    categories: Optional[str]

    try:
        location = args[0]
        categories = args[1] if len(args) > 1 else None
    except IndexError:
        error = {"text": "not enough args"}
        return SlackHookResponse(**error)

    random_restaurants = await yelp.get_random_restaurants(
        location, search_terms=categories
    )
    return SlackHookResponse(
        **{
            "text": "Sorry! Couldn't seem to fetch restaurants.",
            "blocks": yelp_restaurants_to_blocks(random_restaurants),
        }
    )
