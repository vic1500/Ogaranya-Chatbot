from typing import Any

from pydantic import BaseModel

class ChatResponse(BaseModel):
    reply: str

class UserInput(BaseModel):
    input_text: str