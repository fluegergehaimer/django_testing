"""Модуль с тестами проверки маршрутов приложения."""
from http import HTTPStatus


import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


ADMIN_CLIENT = lazy_fixture('admin_client')
CLIENT = lazy_fixture('client')
AUTHOR_CLIENT = lazy_fixture('author_client')


@pytest.mark.parametrize(
    'url, user, status', ((lazy_fixture('users_signup_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_login_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_logout_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_home_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_detail_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_edit_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.NOT_FOUND),

                          (lazy_fixture('news_delete_url'),
                           ADMIN_CLIENT,
                           HTTPStatus.NOT_FOUND),

                          (lazy_fixture('users_signup_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_login_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_logout_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_home_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_detail_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_edit_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_delete_url'),
                           AUTHOR_CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_signup_url'),
                           CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_login_url'),
                           CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('users_logout_url'),
                           CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_home_url'),
                           CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_detail_url'),
                           CLIENT,
                           HTTPStatus.OK),

                          (lazy_fixture('news_edit_url'),
                           CLIENT,
                           HTTPStatus.FOUND),

                          (lazy_fixture('news_delete_url'),
                           CLIENT,
                           HTTPStatus.FOUND),
                          )
                        )
def test_overall_availability(
        url, user, status
):
    """Проверка доступа к страницам всех пользователей."""
    response = user.get(url)

    assert response.status_code == status


@pytest.mark.parametrize(
    'url, redirect_url',
    ((lazy_fixture('news_edit_url'),
      lazy_fixture('edit_redirect_url')),
     (lazy_fixture('news_edit_url'),
      lazy_fixture('edit_redirect_url')),
     (lazy_fixture('news_edit_url'),
      lazy_fixture('edit_redirect_url')),
     (lazy_fixture('news_delete_url'),
      lazy_fixture('delete_redirect_url')),
     ),
)
def test_redirects_for_anonymous_client(client, url, redirect_url):
    """Проверка доступа к страницам редактирования анонимным пользователем."""
    assertRedirects(client.get(url), redirect_url)


@pytest.mark.parametrize(
    'url, user, redirect_url, form_data_to_send',
    ((lazy_fixture('news_detail_url'),
      CLIENT,
      lazy_fixture('news_detail_redirect_url'),
      lazy_fixture('form_data'),
      ),

     (lazy_fixture('news_detail_url'),
      AUTHOR_CLIENT,
      lazy_fixture('news_comment_redirect'),
      lazy_fixture('form_data'),
      ),
     (lazy_fixture('news_edit_url'),
      AUTHOR_CLIENT,
      lazy_fixture('news_comment_redirect'),
      lazy_fixture('form_data'),

      ),
     (lazy_fixture('news_delete_url'),
      AUTHOR_CLIENT,
      lazy_fixture('news_comment_redirect'),
      None,
      ),

     ))
def test_redirect_post_requests(user, url, redirect_url, form_data_to_send):
    """Проверка редиректов при пост запросах."""
    assertRedirects(user.post(url, data=form_data_to_send), redirect_url)
