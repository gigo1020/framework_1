import pytest

from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequestData


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request(self, api_manager: ApiManager, credit_request_data: CreditRequestData, db_session: Session):
        response = api_manager.user_steps.credit_request(credit_request_data, expect_success=True)
        assert response.account_id == credit_request_data.account_id, "Account ID should be equal to response Account ID"
        assert response.balance == response.amount, "Amount should be equal to response balance"

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_data.account_id)
        assert credit_from_db.account_id == credit_request_data.account_id, "Account ID in DB does not match to Account ID"


    def test_credit_request_account_not_found(self, api_manager: ApiManager, credit_request_data: CreditRequestData, db_session: Session):
        invalid_data = credit_request_data.model_copy(update={"account_id": 99999})
        response = api_manager.user_steps.credit_request(invalid_data, expect_success=False)
        assert "not found or does not belong to userid".lower() in response.text.lower()

        credit_from_db = Credit.get_credit_by_account_id(db_session, invalid_data.account_id)
        assert credit_from_db is None, "Credit should not exist in db"

    def test_credit_request_amount_exceeds_limit(self, api_manager: ApiManager, credit_request_data: CreditRequestData, db_session: Session):
        invalid_data = credit_request_data.model_copy(update={"amount": 16500})
        response = api_manager.user_steps.credit_request(invalid_data, expect_success=False)
        assert "amount must be between 5000 and 15000".lower() in response.text.lower()

        credit_from_db = Credit.get_credit_by_account_id(db_session, invalid_data.account_id)
        assert credit_from_db is None, "Credit should not exist in db"
