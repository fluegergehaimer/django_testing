"""Модуль проверки маршрутов приложения."""
from http import HTTPStatus

from django.contrib.auth import get_user_model

from .core import (
    ClientNoteCreation, NOTE_LIST_URL, NOTES_DELETE_URL,
    NOTES_DETAIL_URL, HOMEPAGE_URL, LOGIN_URL,
    LOGOUT_URL, SIGNUP_URL, NOTES_ADD_URL, NOTE_SUCCESS,
    NOTES_EDIT_URL, ADD_REDIRECT_URL, SUCCESS_REDIRECT_URL,
    LIST_REDIRECT_URL, DETAIL_REDIRECT_URL,
    EDIT_REDIRECT_URL, DELETE_REDIRECT_URL
)

User = get_user_model()


class TestRoutes(ClientNoteCreation):
    """Проверка маршрутов приложения."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_pages_availability(self):
        """Страницы доступные всем пользователям."""
        cases = [
            (self.client, HOMEPAGE_URL, HTTPStatus.OK),
            (self.client, LOGIN_URL, HTTPStatus.OK),
            (self.client, LOGOUT_URL, HTTPStatus.OK),
            (self.client, SIGNUP_URL, HTTPStatus.OK),
            (self.reader_client, NOTE_LIST_URL, HTTPStatus.OK),
            (self.reader_client, NOTES_ADD_URL, HTTPStatus.OK),
            (self.reader_client, NOTE_SUCCESS, HTTPStatus.OK),
            (self.reader_client, NOTES_DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, NOTES_EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, NOTES_DELETE_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, NOTES_DETAIL_URL, HTTPStatus.OK),
            (self.author_client, NOTES_EDIT_URL, HTTPStatus.OK),
            (self.author_client, NOTES_DELETE_URL, HTTPStatus.OK),
        ]
        for client, url, status in cases:
            with self.subTest(url=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректа не авторизованного пользователя."""
        adress = (
            (NOTES_ADD_URL, ADD_REDIRECT_URL),
            (NOTE_SUCCESS, SUCCESS_REDIRECT_URL),
            (NOTE_LIST_URL, LIST_REDIRECT_URL),
            (NOTES_DETAIL_URL, DETAIL_REDIRECT_URL),
            (NOTES_DELETE_URL, DELETE_REDIRECT_URL),
            (NOTES_EDIT_URL, EDIT_REDIRECT_URL),
        )
        for url, redirect in adress:
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(self.client.get(url), redirect)
