"""Модуль проверки маршрутов приложения."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .core import (
    Creation, NOTE_LIST_URL, NOTES_DELETE_URL,
    NOTES_DETAIL_URL, HOMEPAGE_URL, LOGIN_URL,
    LOGOUT_URL, SIGNUP_URL, NOTES_ADD_URL, NOTE_SUCCESS,
    NOTES_EDIT_URL
)

User = get_user_model()


class TestRoutes(Creation):
    """Проверка маршрутов приложения."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_pages_availability(self):
        """Страницы доступные всем пользователям."""
        test_list = [
            (
                self.client,
                (HOMEPAGE_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL)
            ),
            (
                self.reader_client,
                (NOTE_LIST_URL, NOTES_ADD_URL, NOTE_SUCCESS)
            ),
            (
                self.author_client,
                (NOTES_DETAIL_URL, NOTES_EDIT_URL, NOTES_DELETE_URL)
            ),
        ]
        for client, urls in test_list:
            for url in urls:
                with self.subTest(url=url):
                    self.assertEqual(
                        client.get(url).status_code,
                        HTTPStatus.OK
                    )

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректа не авторизованного пользователя."""
        adress = (
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:list', None),
            ('notes:add', None),
            ('notes:success', None),
        )
        for key, value in adress:
            with self.subTest(key=key):
                url = reverse(key, args=value)
                redirect_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
