import random

import pytest
from sqlalchemy.orm import Session

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

        assert response.from_account_id == two_users_with_non_empty_accounts.account_a_id
        assert response.to_account_id == two_users_with_non_empty_accounts.account_b_id
        assert response.from_account_id_balance == two_users_with_non_empty_accounts.balance_a_before - transfer_data.amount

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
        invalid_amount = round(two_users_with_non_empty_accounts.balance_a_before + 200.0, 2)
        transfer_data.amount = invalid_amount

        response = api_manager.user_steps.transfer(transfer_data, expect_success=False)

        assert "Insufficient funds".lower() in response.text.lower()

        transaction_in_db = Transaction.get_latest_transaction_by_from_account_id(db_session, two_users_with_non_empty_accounts.account_a_id)
        assert transaction_in_db is None, "Transaction in DB should not exist"