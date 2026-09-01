from datetime import datetime

from pydantic import Field, AliasChoices

from src.main.api.models.base_model import BaseModel

class Credit(BaseModel):
    credit_id: int = Field(..., alias="creditId")
    account_id: int = Field(..., validation_alias=AliasChoices("accountId", "id"))
    amount: int
    term_months: int = Field(..., alias="termMonths")
    balance: int
    created_at: datetime = Field(..., alias="createdAt")

class CreditHistoryResponse(BaseModel):
    user_id: int = Field(..., alias="userId")
    credits: list[Credit] = Field(max_length=1)