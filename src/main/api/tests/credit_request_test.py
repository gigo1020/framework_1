import pytest
from sqlalchemy.orm import Session

from src.main.api.factories.credit_factory import CreditFactory
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

    def test_credit_request_account_not_found(self,
                                              api_manager: ApiManager,
                                              credit_request_data: CreditRequestData,
                                              db_session: Session
                                              ):
        credit_request_data.account_id = CreditFactory.invalid_account_id()

        db_credits_before = Credit.account_credits_count(db_session, credit_request_data.account_id)

        response = api_manager.user_steps.credit_request(credit_request_data, expect_success=False)

        db_credits_after = Credit.account_credits_count(db_session, credit_request_data.account_id)

        assert "not found or does not belong to userid".lower() in response.text.lower()
        assert db_credits_before == db_credits_after, "No new credits should be created"

    def test_credit_request_amount_exceeds_limit(self,
                                                 api_manager: ApiManager,
                                                 credit_request_data: CreditRequestData,
                                                 db_session: Session
                                                 ):
        credit_request_data.amount = CreditFactory.amount_greater_than_maximum()

        db_credits_before = Credit.account_credits_count(db_session, credit_request_data.account_id)  # счетчик кредитов до запроса
        account_from_db_before = Credit.get_credit_by_account_id(db_session,
                                                                 credit_request_data.account_id)  # состояние счета до запроса

        response = api_manager.user_steps.credit_request(credit_request_data, expect_success=False)

        db_credits_after = Credit.account_credits_count(db_session, credit_request_data.account_id)  # счетчик кредитов после запроса
        account_from_db_after = Credit.get_credit_by_account_id(db_session,
                                                                credit_request_data.account_id)  # состояние счета после запроса

        assert "amount must be between 5000 and 15000".lower() in response.text.lower()
        assert db_credits_before == db_credits_after, "No new credits should be created"
        assert account_from_db_before == account_from_db_after, "No changes should be made to the account in DB"

    def test_credit_request_amount_below_limit(self,
                                               api_manager: ApiManager,
                                               credit_request_data: CreditRequestData,
                                               db_session: Session
                                               ):
        credit_request_data.amount = CreditFactory.amount_less_than_minimum()

        db_credits_before = Credit.account_credits_count(db_session, credit_request_data.account_id)  # счетчик кредитов до запроса
        account_from_db_before = Credit.get_credit_by_account_id(db_session,
                                                                 credit_request_data.account_id)  # состояние счета до запроса

        response = api_manager.user_steps.credit_request(credit_request_data, expect_success=False)

        db_credits_after = Credit.account_credits_count(db_session, credit_request_data.account_id)  # счетчик кредитов после запроса
        account_from_db_after = Credit.get_credit_by_account_id(db_session,
                                                                credit_request_data.account_id)  # состояние счета после запроса

        assert "amount must be between 5000 and 15000".lower() in response.text.lower()
        assert db_credits_before == db_credits_after, "No new credits should be created"
        assert account_from_db_before == account_from_db_after, "No changes should be made to the account in DB"
