"""Модуль с фикстурами для тестов."""
import pytest

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.urls import reverse


from news.models import Comment, News


COMMENT_COUNT = 10


@pytest.fixture
def author(django_user_model):
    """Создание объекта пользователя."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    """Клиент савторизованным пользователем."""
    client.force_login(author)
    return client


@pytest.fixture
def news():
    """Создание объекта новости."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def news_id(news):
    """Возврат идентификатора новости."""
    return news.id


@pytest.fixture
def comment(author, news):
    """Создание объекта комментария."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def form_data():
    """Возврат формы комментария."""
    return {'text': 'Текст комментария'}


@pytest.fixture
def news_list():
    """Создание списка новостей."""
    news_list = News.objects.bulk_create(
        News(
            title=f'Заголовок {i}',
            text=f'Текст {i}',
            date=datetime.today() - timedelta(days=i),
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_list


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
    return comment_list


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
def news_detail_redirect_url(users_login_url, comment):
    """Возврат редиректа для логина и перехода к 'news:detail'."""
    next_url = reverse('news:detail', args=(comment.pk,))
    return f"{users_login_url}?next={next_url}"


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
