import random

import pytest

from src.main.api.fixtures.object_fixture import created_obj
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.role import Role
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_data import CreditData
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.models.credit_request import CreditRequest, CreditRequestData
from src.main.api.models.deposit_account_request import DepositAccountData
from src.main.api.models.transfer_request import TransferContext, TransferRequestData
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.fixture
def user_request_data() -> CreateUserRequest:
    """Создаёт данные для пользователя с ролью ROLE_USER и возвращает объект CreateUserRequest"""
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = Role.ROLE_USER.value
    return user_request

@pytest.fixture
def create_user_request(api_manager, created_obj) -> CreateUserRequest:
    """Создаёт пользователя с ролью ROLE_USER и возвращает объект CreateUserRequest"""
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = Role.ROLE_USER.value
    user_response = api_manager.admin_steps.create_user(user_request)
    created_obj.append(user_response)
    return user_request

@pytest.fixture
def user_with_account(api_manager, created_obj) -> DepositAccountData:
    """Создаёт пользователя с ролью ROLE_USER, создаёт ему счет и возвращает объект DepositAccountData"""
    user = RandomModelGenerator.generate(CreateUserRequest)
    user.role = Role.ROLE_USER.value
    user_response = api_manager.admin_steps.create_user(user)
    created_obj.append(user_response)

    auth_headers = RequestSpecs.auth_headers(user.username, user.password) # Логинимся
    account_response = api_manager.user_steps.create_account(user) # Создаём счет

    return DepositAccountData(
        account_id=account_response.id,
        amount=None,
        auth_headers=auth_headers
    )

@pytest.fixture
def two_users_with_non_empty_accounts(api_manager, created_obj) -> TransferContext:
    """Создаёт двух пользователей с ролью ROLE_USER, создаёт им счета и пополняет их баланс на случайную сумму. Возвращает словарь с auth_headers, account_id и balance для каждого пользователя."""
    user_a = RandomModelGenerator.generate(CreateUserRequest) # создать данные пользователя
    user_a.role = Role.ROLE_USER.value
    user_a_response = api_manager.admin_steps.create_user(user_a) # создать пользователя
    created_obj.append(user_a_response) # добавить в список созданных объектов, чтобы после теста он удалился
    auth_a = RequestSpecs.auth_headers(user_a.username, user_a.password) # логин пользователя
    account_a = api_manager.user_steps.create_account(user_a) # создать счет юзеру

    deposit_data_a = DepositAccountData(
        account_id=account_a.id,
        amount=None,
        auth_headers=auth_a
    )
    deposit_response_a, amount_a = api_manager.user_steps.deposit(deposit_data_a, expect_success=True) # пополнить счет юзеру
    balance_a = deposit_response_a.balance # баланс на счете юзера

    user_b = RandomModelGenerator.generate(CreateUserRequest) # аналогично со вторым пользователем
    user_b.role = Role.ROLE_USER.value
    user_b_response = api_manager.admin_steps.create_user(user_b)
    created_obj.append(user_b_response)
    auth_b = RequestSpecs.auth_headers(user_b.username, user_b.password)
    account_b = api_manager.user_steps.create_account(user_b)

    deposit_data_b = DepositAccountData(
        account_id=account_b.id,
        amount=None,
        auth_headers=auth_b
    )
    deposit_response_b, amount_b = api_manager.user_steps.deposit(deposit_data_b, expect_success=True)
    balance_b = deposit_response_b.balance

    return TransferContext(
        auth_a=auth_a,
        account_a_id=account_a.id,
        balance_a_before=balance_a,
        account_b_id=account_b.id,
        balance_b_before=balance_b
    )

@pytest.fixture
def transfer_data(two_users_with_non_empty_accounts) -> TransferRequestData:
    """Возвращает готовый объект TransferRequestData для степа"""
    transfer_valid_amount = round(random.uniform(500.0, min(two_users_with_non_empty_accounts.balance_a_before, 10000.0)), 2)

    return TransferRequestData(
        from_account_id=two_users_with_non_empty_accounts.account_a_id,
        to_account_id=two_users_with_non_empty_accounts.account_b_id,
        amount=transfer_valid_amount,
        auth_headers=two_users_with_non_empty_accounts.auth_a
    )

@pytest.fixture
def credit_role_user_with_account(api_manager, created_obj, create_user_request) -> dict:
    """Создаёт пользователя с ролью ROLE_CREDIT_SECRET, создаёт ему счет и возвращает словарь с auth_headers и account_id"""
    user = RandomModelGenerator.generate(CreateUserRequest) # генерация валидных данных
    user.role = Role.ROLE_CREDIT_SECRET.value # роль кредит
    user_response = api_manager.admin_steps.create_user(user) # создание юзера через админа
    created_obj.append(user_response) # добавление к списку созданных объектов, чтобы потом объект удалился

    auth_headers = RequestSpecs.auth_headers(user.username, user.password)  # Логинимся
    account_response = api_manager.user_steps.create_account(user)  # Создаём счет
    return {
        "auth_headers": auth_headers,
        "account_id": account_response.id
    }

@pytest.fixture
def credit_request_data(api_manager, credit_role_user_with_account) -> CreditRequestData:
    """Возвращает объект CreditRequestData для степа"""
    return CreditRequestData(
        account_id=credit_role_user_with_account["account_id"],
        auth_headers=credit_role_user_with_account["auth_headers"]
    )

@pytest.fixture
def credit_data(api_manager, credit_role_user_with_account) -> CreditData:
    """Создаёт кредит для пользователя с ролью ROLE_CREDIT_SECRET и возвращает объект CreditData"""
    credit_request_data = CreditRequestData(
        account_id=credit_role_user_with_account["account_id"],
        auth_headers=credit_role_user_with_account["auth_headers"]
    )
    credit_response = api_manager.user_steps.credit_request(credit_request_data, expect_success=True)

    return CreditData(
        credit_id=credit_response.credit_id,
        account_id=credit_response.account_id,
        amount=credit_response.amount,
        auth_headers=credit_role_user_with_account["auth_headers"]
    )

