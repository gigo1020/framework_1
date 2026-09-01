from datetime import datetime, timezone
from pydantic import Field

from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel): #API
    from_account_id: int = Field(..., alias="fromAccountId")
    to_account_id: int = Field(..., alias="toAccountId")
    amount: float


class TransferContext(BaseModel):
    auth_a: dict
    account_a_id: int
    balance_a_before: float
    account_b_id: int
    balance_b_before: float
    # created_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TransferRequestData(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    auth_headers: dict
