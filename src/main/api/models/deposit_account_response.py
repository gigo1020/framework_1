from pydantic import Field
from typing import Annotated

from src.main.api.models.base_model import BaseModel


class DepositAccountResponse(BaseModel):
    account_id: int = Field(..., alias="id")
    balance: Annotated[float, Field(ge=0.0)]