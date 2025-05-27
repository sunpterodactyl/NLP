from pydantic import BaseModel, HttpUrl, Field
from typing import List, Union
from enum import Enum

class ModelName(str, Enum):
    GPT4_O = "gpt-4o"
    GPT4_O_MINI = "gpt-4o-mini"

class QueryInput(BaseModel):
    query: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.GPT4_O_MINI)

class SlideSchema(BaseModel):
    title: str
    bullet_points: List[str]
    slide_content: str
    image: bool

class SlideResponse(BaseModel):
    content: List[SlideSchema]

class QueryResponse(BaseModel):
    response: SlideResponse
    session_id: str = Field(default=None)
    model: ModelName = Field(default = ModelName.GPT4_O_MINI)

class DeleteSummary(BaseModel):
    id: int

class IndexInput(BaseModel):
    urls: Union[HttpUrl, List[HttpUrl]]
    session_id: str
