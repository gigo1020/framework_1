from pydantic import Field
from typing import Annotated

from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    account_id: int = Field(..., alias="accountId")
    amount: float | None

class DepositAccountData(BaseModel):
    account_id: int
    amount: float | None
    auth_headers: dict | None