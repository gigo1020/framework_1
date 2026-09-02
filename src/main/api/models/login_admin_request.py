from src.main.api.models.base_model import BaseModel

class LoginAdminRequest(BaseModel):
    username: str = "admin"
    password: str = "123456"