from src.main.api.models.base_model import BaseModel


class CreditData(BaseModel):
    credit_id: int | None
    account_id: int | None
    amount: int | None
    auth_headers: dict | None