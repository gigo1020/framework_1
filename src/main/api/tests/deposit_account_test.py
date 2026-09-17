import pytest
from sqlalchemy.orm import Session

from src.main.api.factories.deposit_factory import DepositFactory
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_account_request import DepositAccountData
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_valid_amount(self,
                                  api_manager: ApiManager,
                                  user_with_account: DepositAccountData,
                                  db_session: Session
                                  ):
        response, response_amount = api_manager.user_steps.deposit(user_with_account, expect_success=True)

        assert response.account_id == user_with_account.account_id, "Account ID does not match."
        assert response.balance == response_amount, "Balance should be equal to response amount."

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == response.account_id, "Account ID in DB should be equal to response ID."
        assert account_in_db.balance == response_amount, "Balance in DB should be equal to response amount."

    def test_deposit_unauthorized(self,
                                  api_manager: ApiManager,
                                  user_with_account: DepositAccountData,
                                  db_session: Session
                                  ):
        user_with_account.auth_headers = DepositFactory.empty_auth_headers()

        response = api_manager.user_steps.deposit(user_with_account, expect_success=False)

        assert "JWT Token not found".lower() in response[
            0].text.lower(), "Response should contain 'JWT Token not found' message."

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == user_with_account.account_id, "Account ID in DB should be equal to account ID."

    @pytest.mark.parametrize("boundary_invalid_amount",
                             DepositFactory.boundary_invalid_amounts()
                             )
    def test_deposit_boundary_invalid_amount(self,
                                             api_manager: ApiManager,
                                             user_with_account: DepositAccountData,
                                             boundary_invalid_amount: float,
                                             db_session: Session
                                             ):
        user_with_account.amount = boundary_invalid_amount

        response = api_manager.user_steps.deposit(user_with_account, expect_success=False)

        assert "amount must be between 1000 and 9000".lower() in response[
            0].text.lower(), "Response should contain 'amount must be between 1000 and 9000' message."

        account_in_db = Account.get_account_by_id(db_session, user_with_account.account_id)
        assert account_in_db.id == user_with_account.account_id, "Account ID in DB should be equal to account ID."

    def test_deposit_random_invalid_amount(self,
                                           api_manager: ApiManager,
                                           user_with_account: DepositAccountData,
                                           db_session: Session
                                           ):
        user_with_account.amount = DepositFactory.invalid_amount()
        account_in_db_before = Account.get_account_by_id(db_session, user_with_account.account_id)

        response = api_manager.user_steps.deposit(user_with_account, expect_success=False)

        account_in_db_after = Account.get_account_by_id(db_session, user_with_account.account_id)

        assert "amount must be between 1000 and 9000".lower() in response[
            0].text.lower(), "Response should contain 'amount must be between 1000 and 9000' message."
        assert account_in_db_before == account_in_db_after, "No changes should be made to the account in DB"
