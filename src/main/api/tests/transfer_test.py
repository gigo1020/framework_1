import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.factories.transfer_factory import TransferFactory
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.transfer_request import TransferRequestData, TransferContext
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransfer:
    def test_transfer_between_users(self,
                                    api_manager: ApiManager,
                                    two_users_with_non_empty_accounts: TransferContext,
                                    transfer_data: TransferRequestData,
                                    db_session: Session
                                    ):
        response = api_manager.user_steps.transfer(transfer_data, expect_success=True)

        assert response.from_account_id == two_users_with_non_empty_accounts.account_a_id, "from_account_id doesn't match"
        assert response.to_account_id == two_users_with_non_empty_accounts.account_b_id, "to_account_id doesn't match"
        assert response.from_account_id_balance == two_users_with_non_empty_accounts.balance_a_before - transfer_data.amount, "Incorrect balance in response"

        transaction_in_db = Transaction.get_latest_transaction_by_from_account_id(db_session, two_users_with_non_empty_accounts.account_a_id)
        assert transaction_in_db.from_account_id == response.from_account_id, "From_account_id in DB should be equal to from_account_id"
        assert transaction_in_db.to_account_id == response.to_account_id, "To_account_id in DB should be equal to to_account_id"
        assert transaction_in_db.amount == transfer_data.amount, "Amount in DB should be equal to amount"

    def test_transfer_between_users_insufficient_funds(self,
                                                       api_manager: ApiManager,
                                                       two_users_with_non_empty_accounts: TransferContext,
                                                       transfer_data: TransferRequestData,
                                                       db_session: Session
                                                       ):
        transfer_data.amount = TransferFactory.insufficient_amount(two_users_with_non_empty_accounts.balance_a_before)

        account_a_from_bd_before = Account.get_account_by_id(db_session, two_users_with_non_empty_accounts.account_a_id) # состояние счета отправителя до запроса
        account_b_from_bd_before = Account.get_account_by_id(db_session, two_users_with_non_empty_accounts.account_b_id) # состояние счета получателя до запроса
        transactions_count_before = Transaction.transactions_count(db_session,
                                                                   two_users_with_non_empty_accounts.account_a_id) # счетчик транзакций до запроса

        response = api_manager.user_steps.transfer(transfer_data, expect_success=False)

        account_a_from_bd_after = Account.get_account_by_id(db_session, two_users_with_non_empty_accounts.account_a_id) # состояние счета отправителя после запроса
        account_b_from_bd_after = Account.get_account_by_id(db_session, two_users_with_non_empty_accounts.account_b_id) # состояние счета получателя после запроса
        transactions_count_after = Transaction.transactions_count(db_session,
                                                                  two_users_with_non_empty_accounts.account_a_id) # счетчик транзакций после запроса

        assert "Insufficient funds".lower() in response.text.lower(), "Insufficient funds error message should be in response"
        assert transactions_count_before == transactions_count_after, "No new transactions should be created"
        assert account_a_from_bd_before == account_a_from_bd_after, "No changes should be made to the from_account in DB"
        assert account_b_from_bd_before == account_b_from_bd_after, "No changes should be made to the to_account in DB"