from pydantic import BaseModel, Field
from typing import List, Optional

from pydantic import BaseModel, Field

class CheckRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class CheckResponse(BaseModel):
    corrected_text: str


class Match(BaseModel):
    message: str
    shortMessage: Optional[str] = None
    offset: int
    length: int
    replacements: List[Replacement]
    rule_id: str
    category: str
    issueType: str

class CheckResponse(BaseModel):
    corrected_text: str
    matches: List[Match]

class SuggestRequest(BaseModel):
    text: str

class SuggestResponse(BaseModel):
    suggestions: List[str]
