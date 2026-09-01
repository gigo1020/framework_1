from typing import Optional

import requests
import allure
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    """Класс для выполнения CRUD-запросов (Create, Read, Update, Delete) к API"""
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump(by_alias=True) if model is not None else ""

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(
                str(body),
                "Request Body",
                allure.attachment_type.JSON
            )

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            json=body,
            headers=self.request_spec
        )

        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
        self.response_spec = response
        return response

    def delete(self, user_id: int) -> Response:
        """Удаляет пользователя по его ID"""

        with allure.step(f"DELETE {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(
                str(user_id),
                "Request Body",
                allure.attachment_type.JSON
            )

        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
        self.response_spec = response
        return response

    def get(self) -> Response:
        """Выполняет GET-запрос к API"""

        with allure.step(f"GET {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(
                str(self.request_spec),
                "Request Headers",
                allure.attachment_type.JSON
            )

        response = requests.get(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec
        )
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
        self.response_spec = response
        return response
