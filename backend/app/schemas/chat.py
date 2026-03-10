from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str

class UserInput(BaseModel):
    input_text: str