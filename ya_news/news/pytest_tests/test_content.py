"""Модуль с тестами проверки контента приложения."""
import pytest

from django.conf import settings
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_page(client, news_home_url):
    """Проверка вывода количества новостей на странице."""
    response = client.get(news_home_url)
    news_count = len(response.context['object_list'])
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_order(client, news_home_url):
    """Проверка сортировки новостей."""
    news_date = [
        news.date for news in client.get(
            news_home_url
        ).context['object_list']
    ]
    assert news_date == sorted(news_date, reverse=True)


@pytest.mark.django_db
@pytest.mark.usefixtures('comment_list')
def test_comments_order(client, news_detail_url):
    """Проверка сортировки комментариев по времени."""
    all_comments = client.get(
        news_detail_url
    ).context['news'].comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'user, access',
    (
        (lazy_fixture('author_client'), True),
        (lazy_fixture('client'), False),
    )
)
@pytest.mark.django_db
def test_forms_of_anon_and_authorised_users(user, access, news_detail_url):
    """Проверка формы для отправки комментариев."""
    assert ('form' in user.get(news_detail_url).context) == access
