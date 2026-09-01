from typing import Optional

from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRequest(BaseModel):
    account_id: int = Field(..., alias="accountId")
    amount: int
    term_months: int = Field(alias="termMonths")

class CreditRequestData(BaseModel):
    account_id: int
    auth_headers: dict
    amount: Optional[int] = None
    term_months: Optional[int] = None