from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRepayResponse(BaseModel):
    credit_id: int = Field(..., alias='creditId')
    amount_deposited: int = Field(..., alias='amountDeposited')