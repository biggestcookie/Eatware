from core.voting import send_vote_message
import json
from collections import ChainMap
from typing import Dict

from fastapi import APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from models.dialogflow import WebhookRequest, WebhookResponse
from services import yelp

router = APIRouter()


@router.post("", response_model=WebhookResponse)
async def post(
    body: WebhookRequest, background_tasks: BackgroundTasks
) -> WebhookResponse:
    print(json.dumps(jsonable_encoder(body), indent=4, sort_keys=True))
    pastContexts = body.queryResult.outputContexts
    args = {
        **body.queryResult.parameters,
    }
    if pastContexts and len(pastContexts) > 0:
        for context in pastContexts:
            args = dict(ChainMap(args, context["parameters"]))

    channel: str
    try:
        channel = body.originalDetectIntentRequest["payload"]["data"]["event"][
            "channel"
        ]
    except KeyError:
        channel = ""
    return await fulfill_for_intent(
        body.queryResult.intent["displayName"], args, channel, background_tasks,
    )


async def fulfill_for_intent(
    intent_name: str, args: Dict, channel: str, background_tasks: BackgroundTasks,
) -> WebhookResponse:
    """Calls function mapped for each intent, passing parameters to the function as args"""
    func_for_intent = INTENT_FUNCTIONS.get(intent_name)
    if not func_for_intent:
        raise HTTPException(404, "No method for that intent")
    return await func_for_intent(args, channel, background_tasks)


async def example_fulfillment(args: Dict) -> WebhookResponse:
    return WebhookResponse(
        **{"fulfillmentText": f"Test succeeded. {args.get('number')}"}
    )


def dict_to_str(dict: Dict) -> Dict:
    for key, value in dict.items():
        if isinstance(value, list):
            dict[key] = " ".join(value)
    return dict


async def request_fulfillment(
    args: Dict, channel: str, background_tasks: BackgroundTasks,
) -> WebhookResponse:
    """Feeds Dialogflow parameters to Yelp, then returns Dialogflow response with Slack payload"""
    args = dict_to_str(args)
    food = args.get("food")
    restrictions = args.get("restrictions")
    address = args.get("address")
    price = args.get("price") or "1,2"
    status = args.get("status") or ""
    categories = f"{food} {restrictions} {status}"
    random_restaurants = []
    try:
        random_restaurants = await yelp.get_random_restaurants(
            address, search_terms=categories, price=price
        )
    except Exception:
        pass

    if not random_restaurants:
        return WebhookResponse(
            **{
                "fulfillmentText": f"Sorry! Couldn't find anything for {categories} in your area. Tag me again to start over."
            }
        )
    try:
        background_tasks.add_task(send_vote_message, channel, random_restaurants)
        return WebhookResponse(
            **{"fulfillmentText": "Sure thing! Let me pull up some restaurants."}
        )
    except Exception:
        return WebhookResponse(
            **{
                "fulfillmentText": "Sorry! Service seems to be offline right now. Try again in a moment."
            }
        )


INTENT_FUNCTIONS = {
    "api-test-intent": example_fulfillment,
    "restaurant-search - yes": request_fulfillment,
    "restaurant-search - more": request_fulfillment,
}
