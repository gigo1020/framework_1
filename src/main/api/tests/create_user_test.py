import pytest
from sqlalchemy.orm import Session

from src.main.api.factories.user_credentials_factory import UserCredentialsFactory
from src.main.api.classes.api_manager import ApiManager
from src.main.api.foundation.role import Role
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self,
                               api_manager: ApiManager,
                               user_request_data: CreateUserRequest,
                               created_obj,
                               db_session: Session
                               ):
        response = api_manager.admin_steps.create_user(user_request_data, expect_success=True)
        created_obj.append(response)

        assert user_request_data.username == response.username
        assert user_request_data.role == response.role

        user_from_db = User.get_user_by_username(db_session, response.username)
        assert user_from_db.username == response.username, "User should be created in the database with the correct username"

    @pytest.mark.parametrize(
        "username, password",
        UserCredentialsFactory.invalid_user_credentials()
    )
    def test_create_user_invalid(self,
                                 username: str,
                                 password: str,
                                 api_manager: ApiManager,
                                 db_session: Session
                                 ):
        user_request_data = CreateUserRequest(username=username, password=password, role=Role.ROLE_USER.value)

        api_manager.admin_steps.create_user(user_request_data, expect_success=False)

        user_from_db = User.get_user_by_username(db_session, username)
        assert user_from_db is None, "User should not be created in the database for invalid input"
