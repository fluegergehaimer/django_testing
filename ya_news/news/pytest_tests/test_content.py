"""Модуль с тестами проверки контента приложения."""
import pytest

from django.conf import settings

from news.forms import CommentForm


def test_news_page(client, news_home_url, news_list):
    """Проверка вывода количества новостей на странице."""
    assert len(
        client.get(news_home_url).context['object_list']
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home_url, news_list):
    """Проверка сортировки новостей."""
    news_date = [
        news.date for news in client.get(
            news_home_url
        ).context['object_list']
    ]
    assert news_date == sorted(news_date, reverse=True)


def test_comments_order(client, news_detail_url, comment_list):
    """Проверка сортировки комментариев по времени."""
    comment_list_dates = [
        comment.created for comment in client.get(
            news_detail_url
        ).context['news'].comment_set.all()]
    assert comment_list_dates == sorted(comment_list_dates)


def test_anonymous_client_has_no_form(client, news_detail_url):
    """Проверка дуступности формы не авторизованному пользователю."""
    assert 'form' not in client.get(news_detail_url).context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news_detail_url):
    """Проверка дуступности формы авторизованному пользователю."""
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
