import random
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.deposit_account_request import DepositAccountData
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_valid_amount(self, api_manager: ApiManager, user_with_account: DepositAccountData, db_session: Session):
        response, response_amount = api_manager.user_steps.deposit(user_with_account, expect_success=True)

        assert response.account_id == user_with_account.account_id, "Account ID does not match."
        assert response.balance == response_amount, "Balance should be equal to response amount."

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == response.account_id, "Account ID in DB should be equal to response ID."
        assert account_in_db.balance == response_amount, "Balance in DB should be equal to response amount."

    def test_deposit_unauthorized(self, api_manager: ApiManager, user_with_account: DepositAccountData, db_session: Session):
        user_with_account.auth_headers = {}
        response = api_manager.user_steps.deposit(user_with_account, expect_success=False)

        assert "JWT Token not found".lower() in response[0].text.lower()

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == user_with_account.account_id, "Account ID in DB should be equal to account ID."


    @pytest.mark.parametrize("invalid_amount",
                                 [
                                  505.05,
                                  998.0,
                                  999.99,
                                  9000.01,
                                  9001.00,
                                  14500.00
                                 ]
                             )
    def test_deposit_invalid_amount(self, api_manager: ApiManager, user_with_account: DepositAccountData, invalid_amount, db_session: Session):
        user_with_account.amount = invalid_amount
        response = api_manager.user_steps.deposit(user_with_account, expect_success=False)

        assert "amount must be between 1000 and 9000".lower() in response[0].text.lower()

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == user_with_account.account_id, "Account ID in DB should be equal to account ID."

