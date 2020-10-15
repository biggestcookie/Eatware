from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QueryResult(BaseModel):
    queryText: str
    languageCode: str
    speechRecognitionConfidence: Optional[float]
    action: Optional[Any]
    parameters: Dict
    allRequiredParamsPresent: bool
    fulfillmentText: Optional[str]
    fulfillmentMessages: Optional[List[Any]]
    webhookSource: Optional[str]
    webhookPayload: Optional[Any]
    outputContexts: Optional[List[Any]]
    intent: Dict
    intentDetectionConfidence: float
    diagnosticInfo: Optional[Any]
    sentimentAnalysisResult: Optional[Any]


class WebhookRequest(BaseModel):
    session: str
    response: Optional[str]
    queryResult: QueryResult
    originalDetectIntentRequest: Any


class WebhookResponse(BaseModel):
    fulfillmentText: Optional[str]
    fulfillmentMessages: Optional[List[Any]]
    source: Optional[str]
    payload: Optional[Any]
    outputContexts: Optional[Any]
    followupEventInput: Optional[Any]
    sessionEntityTypes: Optional[Any]
