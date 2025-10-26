from pydantic import BaseModel
from typing import Literal

class IntentClassificationResponse(BaseModel):
    intent: Literal[
        "search_recommendation",
        "compare",
        "details",
        "query",
        "chitchat",
        "irrelevant",
        "adversarial"
    ]
