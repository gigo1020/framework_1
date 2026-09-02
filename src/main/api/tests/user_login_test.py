import pytest
from sqlalchemy.orm import Session

from src.main.api.models.login_admin_request import LoginAdminRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.foundation.role import Role
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager, db_session: Session):
        login_admin_request = LoginAdminRequest()

        response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_request.username == response.user.username, "Username should be the same"
        assert response.user.role == Role.ROLE_ADMIN.value, "Role should be ROLE_ADMIN"

        user_from_db = User.get_user_by_username(db_session, login_admin_request.username)
        assert user_from_db.username == response.user.username, "Username in DB should be the same"
        assert user_from_db.role == Role.ROLE_ADMIN.value, "Role in DB should be ROLE_ADMIN"


    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, "Username should be the same"
        assert response.user.role == "ROLE_USER", "Role should be ROLE_USER"

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == response.user.username, "Username in DB should be the same"
        assert user_from_db.role == Role.ROLE_USER.value, "Role in DB should be ROLE_USER"

