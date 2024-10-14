from urllib.parse import urlencode

import structlog
import httpx

from api_client.exceptions import NotesAPIException
from api_client.variables import NOTES_API_URL

logger = structlog.get_logger(__name__)


class NotesAPIClient:
    _BASE_URL = NOTES_API_URL
    _SET_TELEGRAM_ID_URL = '/api/telegram/set_telegram_id'
    _AUTH_URL = '/api/telegram/auth'
    _NOTES_URL = '/api/notes'

    _client = httpx.AsyncClient(verify=False)

    @classmethod
    async def link_telegram_id(cls, token: str, user_id: int) -> dict:
        data = {"token": token, "telegram_id": user_id}
        response = await cls._request(
            method='POST',
            url=cls._build_abosolute_url(cls._SET_TELEGRAM_ID_URL),
            data=data
        )
        return response

    @classmethod
    async def get_notes(cls, telegram_id: int | str) -> dict:
        response = await cls._auth_request(
            telegram_id=telegram_id,
            method='GET',
            url=cls._build_abosolute_url(cls._NOTES_URL),
        )
        return response

    @classmethod
    async def _auth_request(
        cls,
        telegram_id: int | str,
        method: str,
        url: str,
        data: dict | None = None,
        query_params: dict | None = None
    ) -> dict:
        access_token = await cls._get_access_token(telegram_id)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = await cls._request(
            method=method,
            url=url,
            data=data,
            query_params=query_params,
            headers=headers
        )
        return response

    @classmethod
    async def _get_access_token(cls, telegram_id: int | str) -> str:
        query_params = {'telegram_id': telegram_id}
        url = cls._build_abosolute_url(cls._AUTH_URL)
        response = await cls._request(
            method='POST',
            url=url,
            query_params=query_params,
        )
        return response.get('access_token')

    @classmethod
    async def _request(
        cls,
        method: str,
        url: str,
        data: dict | None = None,
        query_params: dict | None = None,
        headers: dict | None = None,
    ) -> dict:

        if query_params:
            url = url + '?' + urlencode(query_params)

        try:
            response = await cls._client.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=10,
                follow_redirects=True
            )
        except (httpx.TimeoutException,) as e:
            raise NotesAPIException("Ошибка при отправке запроса.")
        logger.info('Response', status_code=response.status_code, response=response.text)
        cls._check_response(response)
        response = response.json()
        return response

    @staticmethod
    def _check_response(response: httpx.Response):
        if response.status_code in (200, 201, 202):
            return

        if response.status_code == 400:
            raise NotesAPIException("Синтаксическая ошибка в запросе.")

        if response.status_code == 401:
            raise NotesAPIException("Не достаточно прав.")

        if 400 <= response.status_code < 500:
            raise NotesAPIException("Произошла ошибка.")

        if response.status_code >= 500:
            raise NotesAPIException("Произошла внутренняя ошибка.")

    @classmethod
    def _build_abosolute_url(cls, url: str) -> str:
        return cls._BASE_URL + url
