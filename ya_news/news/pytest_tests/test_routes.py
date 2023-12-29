"""Модуль с тестами проверки маршрутов приложения."""
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


ADMIN_CLIENT = lazy_fixture('admin_client')
CLIENT = lazy_fixture('client')
AUTHOR_CLIENT = lazy_fixture('author_client')
SIGN_UP_URL = lazy_fixture('users_signup_url')
LOGIN_URL = lazy_fixture('users_login_url')
LOGOUT_URL = lazy_fixture('users_logout_url')
HOME_URL = lazy_fixture('news_home_url')
DETAIL_URL = lazy_fixture('news_detail_url')
EDIT_URL = lazy_fixture('news_edit_url')
DELETE_URL = lazy_fixture('news_delete_url')
EDIT_REDIRECT_URL = lazy_fixture('edit_redirect_url')
DELETE_REDIRECT_URL = lazy_fixture('delete_redirect_url')


@pytest.mark.parametrize(
    'url, clients, status', (
        (
            SIGN_UP_URL,
            ADMIN_CLIENT,
            HTTPStatus.OK),
        (
            LOGIN_URL,
            ADMIN_CLIENT,
            HTTPStatus.OK),
        (
            LOGOUT_URL,
            ADMIN_CLIENT,
            HTTPStatus.OK),
        (
            HOME_URL,
            ADMIN_CLIENT,
            HTTPStatus.OK),
        (
            DETAIL_URL,
            ADMIN_CLIENT,
            HTTPStatus.OK),
        (
            EDIT_URL,
            ADMIN_CLIENT,
            HTTPStatus.NOT_FOUND),
        (
            DELETE_URL,
            ADMIN_CLIENT,
            HTTPStatus.NOT_FOUND),
        (
            SIGN_UP_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            LOGIN_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            LOGOUT_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            HOME_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            DETAIL_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            EDIT_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            DELETE_URL,
            AUTHOR_CLIENT,
            HTTPStatus.OK),
        (
            SIGN_UP_URL,
            CLIENT,
            HTTPStatus.OK),
        (
            LOGIN_URL,
            CLIENT,
            HTTPStatus.OK),
        (
            LOGOUT_URL,
            CLIENT,
            HTTPStatus.OK),
        (
            HOME_URL,
            CLIENT,
            HTTPStatus.OK),
        (
            DETAIL_URL,
            CLIENT,
            HTTPStatus.OK),
        (
            EDIT_URL,
            CLIENT,
            HTTPStatus.FOUND),
        (
            DELETE_URL,
            CLIENT,
            HTTPStatus.FOUND),
    )
)
def test_overall_availability(
        url, clients, status
):
    """Проверка доступа к страницам всех пользователей."""
    assert clients.get(url).status_code == status


@pytest.mark.parametrize(
    'url, redirect_url', (
        (EDIT_URL, EDIT_REDIRECT_URL),
        (DELETE_URL, DELETE_REDIRECT_URL,)
    )
)
def test_redirects_for_anonymous_client(client, url, redirect_url):
    """Проверка доступа к страницам редактирования анонимным пользователем."""
    assertRedirects(client.get(url), redirect_url)
