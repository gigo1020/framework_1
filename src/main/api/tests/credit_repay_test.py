import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_data import CreditData


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_data: CreditData, db_session: Session):
        response = api_manager.user_steps.credit_repay(credit_data, expect_success=True)

        assert response.credit_id == credit_data.credit_id, "Credit repay failed"
        assert response.amount_deposited == credit_data.amount, "Credit repay failed"

        credit_from_db = Credit.get_credit_by_id(db_session, response.credit_id)
        assert credit_from_db.account_id == credit_data.account_id, "Account ID in DB does not match."
        assert credit_from_db.id == credit_data.credit_id, "Credit ID in DB does not match."
        assert credit_from_db.amount == credit_data.amount, "Credit in DB amount does not match."

    def test_credit_repay_access_denied(self, api_manager: ApiManager, credit_data: CreditData, db_session: Session):
        credit_data.account_id = 99999
        response = api_manager.user_steps.credit_repay(credit_data, expect_success=False)

        assert f"account {credit_data.account_id} not found or does not belong to userid".lower() in response.text.lower()

        credit_from_db = Credit.get_credit_by_id(db_session, credit_data.credit_id)
        assert credit_from_db.id == credit_data.credit_id, "Credit ID in DB does not match."

    def test_credit_not_found(self, api_manager: ApiManager, credit_data: CreditData, db_session: Session):
        credit_data.credit_id = 99999
        response = api_manager.user_steps.credit_repay(credit_data, expect_success=False)

        assert f"credit with id {credit_data.credit_id} was not found or does not belong to the user".lower() in response.text.lower()

        credit_from_db = Credit.get_credit_by_id(db_session, credit_data.credit_id)
        assert credit_from_db is None, "Credit should not be found in DB."

    def test_credit_repay_insufficient_funds(self, api_manager: ApiManager, credit_data: CreditData, db_session: Session):
        credit_data.amount += 1000.00
        response = api_manager.user_steps.credit_repay(credit_data, expect_success=False)

        assert "insufficient funds".lower() in response.text.lower()

        credit_from_db = Credit.get_credit_by_id(db_session, credit_data.credit_id)
        assert credit_from_db.id == credit_data.credit_id, "Credit ID in DB does not match."
        assert credit_from_db.account_id == credit_data.account_id, "Account ID in DB does not match."
        assert credit_from_db.amount < credit_data.amount, "Credit amount in DB should be less than credit amount."
