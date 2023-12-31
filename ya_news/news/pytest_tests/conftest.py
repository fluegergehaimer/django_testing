"""Модуль с фикстурами для тестов."""
import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


COMMENT_COUNT = 10


@pytest.fixture
def author(django_user_model):
    """Создание объекта пользователя."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    """Клиент с авторизованным пользователем."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news():
    """Создание объекта новости."""
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def comment(author, news):
    """Создание объекта комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def news_list():
    """Создание списка новостей."""
    News.objects.bulk_create(
        News(
            title=f'Заголовок {i}',
            text=f'Текст {i}',
            date=datetime.today() - timedelta(days=i),
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_list(news, author):
    """Создание списка комментариев."""
    for i in range(COMMENT_COUNT):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'Текст комментария {i}',
        )
        comment.created = timezone.now() + timedelta(days=i)
        comment.save()


@pytest.fixture
def users_login_url():
    """Возврат ссылки 'users:login'."""
    return reverse('users:login')


@pytest.fixture
def users_logout_url(news):
    """Возврат ссылки 'users:logout'."""
    return reverse('users:logout')


@pytest.fixture
def users_signup_url(news):
    """Возврат ссылки 'users:signup'."""
    return reverse('users:signup')


@pytest.fixture
def news_home_url(news):
    """Возврат ссылки 'news:home'."""
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    """Возврат ссылки 'news:detail'."""
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_edit_url(comment):
    """Возврат ссылки 'news:edit'."""
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def news_delete_url(comment):
    """Возврат ссылки 'news:delete'."""
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def news_detail_redirect_url(users_login_url, news_detail_url):
    """Возврат редиректа для логина и перехода к 'news:detail'."""
    return f"{users_login_url}?next={news_detail_url}"


@pytest.fixture
def news_comment_redirect(news):
    """Возврат редиректа 'news:detail' и '#comments'."""
    return reverse('news:detail', args=(news.pk,)) + '#comments'


@pytest.fixture
def edit_redirect_url(users_login_url, news_edit_url):
    """Возврат редиректа для логина и перехода к ссылке редактированию."""
    return f'{users_login_url}?next={news_edit_url}'


@pytest.fixture
def delete_redirect_url(users_login_url, news_delete_url):
    """Возврат редиректа для логина и перехода к ссылке удаления."""
    return f'{users_login_url}?next={news_delete_url}'


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(
    db,  # noqa
):
    """Автоматический доступ к базе данных."""
