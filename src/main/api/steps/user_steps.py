import random
from typing import Optional

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_data import CreditData
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest, CreditRequestData
from src.main.api.models.deposit_account_request import DepositAccountRequest, DepositAccountData
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs import response_specs
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, deposit_data: DepositAccountData, expect_success: bool = True):
        if deposit_data.amount is None:
            amount = round(random.randint(1000, 9000), 2)  # генерируем валидную сумму
        else:
            amount = deposit_data.amount

        deposit_request = DepositAccountRequest(
            accountId=deposit_data.account_id,
            amount=amount
        )

        requester = ValidateCrudRequester if expect_success else CrudRequester
        response_spec = ResponseSpecs.request_ok() if expect_success else ResponseSpecs.request_bad()

        response = requester(
            deposit_data.auth_headers,
            Endpoint.DEPOSIT_ACCOUNT,
            response_spec
        ).post(deposit_request)

        return response, amount

    def transfer(self, TransferRequestData, expect_success: bool = True):
        transfer_request = TransferRequest(
            fromAccountId=TransferRequestData.from_account_id,
            toAccountId=TransferRequestData.to_account_id,
            amount=TransferRequestData.amount
        )

        requester = ValidateCrudRequester if expect_success else CrudRequester
        response_spec = ResponseSpecs.request_ok() if expect_success else ResponseSpecs.request_bad()

        return requester(
            TransferRequestData.auth_headers,
            Endpoint.TRANSFER,
            response_spec
        ).post(transfer_request)

    # def transfer_invalid(
    #         self,
    #         from_account_id: int,
    #         to_account_id: int,
    #         amount: float,
    #         auth_headers: dict = {},
    # ):
    #     transfer_request = TransferRequest(
    #         fromAccountId=from_account_id,
    #         toAccountId=to_account_id,
    #         amount=amount
    #     )
    #     return CrudRequester(
    #         auth_headers,
    #         Endpoint.TRANSFER,
    #         ResponseSpecs.request_bad()
    #     ).post(transfer_request)

    def credit_request(self, credit_data: CreditRequestData, expect_success: bool = True):
        amount=credit_data.amount or random.randint(5000, 15000)
        term_months = credit_data.term_months or random.randint(1, 60)

        credit_request = CreditRequest(
            accountId=credit_data.account_id,
            amount=amount,
            termMonths=term_months
        )
        requester = ValidateCrudRequester if expect_success else CrudRequester
        response_spec = ResponseSpecs.request_created() if expect_success else ResponseSpecs.request_bad()

        return requester(
            credit_data.auth_headers,
            Endpoint.CREDIT_REQUEST,
            response_spec
        ).post(credit_request)

    def credit_repay(self, credit_data: CreditData, expect_success: bool = True):
        repay_request = CreditRepayRequest(
            creditId=credit_data.credit_id,
            accountId=credit_data.account_id,
            amount=credit_data.amount
        )
        requester = ValidateCrudRequester if expect_success else CrudRequester
        response_spec = ResponseSpecs.request_ok() if expect_success else ResponseSpecs.request_bad()

        return requester(
            credit_data.auth_headers,
            Endpoint.CREDIT_REPAY,
            response_spec
        ).post(repay_request)

