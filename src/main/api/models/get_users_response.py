from typing import List

from src.main.api.models.base_model import BaseModel

class GetUser(BaseModel):
    id: int
    username: str
    role: str

class GetUsersResponse(BaseModel):
    body: List[GetUser]