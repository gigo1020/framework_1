from pydantic import Field, AliasChoices

from src.main.api.models.base_model import BaseModel


class CreditResponse(BaseModel):
    account_id: int = Field(..., validation_alias=AliasChoices("accountId", "id"))
    amount: int = Field(...)
    term_months: int = Field(..., alias="termMonths")
    balance: int
    credit_id: int = Field(..., alias="creditId")