from typing import List, Optional

from pydantic import BaseModel


class BlockAccessory(BaseModel):
    type = "image"
    image_url: str
    alt_text: str


class BlockText(BaseModel):
    type = "mrkdwn"
    text: Optional[str]


class Block(BaseModel):
    type: str
    text: Optional[BlockText]
    accessory: Optional[BlockAccessory]


class SlackHookResponse(BaseModel):
    text: str
    blocks: Optional[List[Block]]


class SlackHookRequest(BaseModel):
    token: str
    command: str
    text: str
    response_url: str
    trigger_id: str
    user_id: str
    user_name: str
    team_id: str
    team_domain: str
    enterprise_id: str
    channel_id: str
    channel_name: str


class SlackMessageBody(BaseModel):
    token: str
    channel: str
    text: str
    blocks: Optional[List[Block]]
