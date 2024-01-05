"""Модуль с тестами проверки логики приложения."""
from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


FORM_DATA = {'text': 'Текст комментария'}
BAD_WORDS_DATA = {'text': f'Какой-то текст, {choice(BAD_WORDS)}, еще текст.'}


def test_anonym_client_cant_create_comment(
        client,
        news_detail_url,
        news_detail_redirect_url
):
    """Проверка создания коментария не авторизованным пользователем."""
    client.post(news_detail_url, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_authorised_client_can_create_comment(
        author_client,
        news,
        author,
        news_detail_url,
        news_comment_redirect
):
    """Проверка создания коментария авторизованным пользователем."""
    author_client.post(news_detail_url, data=FORM_DATA)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.author == author
    assert new_comment.news == news


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news_detail_url, bad_word):
    """Проверка запрещенных слов."""
    response = author_client.post(
        news_detail_url,
        data=BAD_WORDS_DATA
    )
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client,
        comment,
        news_detail_url
):
    """Проверка редактирования комментария авторизованым пользователем."""
    author_client.post(news_detail_url, data=FORM_DATA)
    updated_comment = Comment.objects.get(id=comment.id)
    assert comment.text == updated_comment.text
    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author


def test_author_can_delete_comment(
        author_client,
        comment,
        news_delete_url,
        news_comment_redirect
):
    """Авторизованный пользователь может удалять свои комментарии."""
    assert Comment.objects.count() != 0
    author_client.post(news_delete_url)
    assert not Comment.objects.filter(pk=comment.pk).exists()
    assert Comment.objects.count() == 0


def test_user_cant_edit_comment_of_another_user(
        admin_client,
        comment,
        news_edit_url
):
    """Проверка доступа только к своим коментариям."""
    comment_count_initial = Comment.objects.count()
    response = admin_client.post(news_edit_url, data=FORM_DATA)
    updated_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_count_initial == Comment.objects.count()
    assert comment.text == updated_comment.text
    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author


def test_author_cant_delete_comment_of_another_user(
        admin_client,
        comment,
        news_delete_url
):
    """Проверка удаления чужих комментариев пользователя."""
    comments_initial = set(Comment.objects.all())
    response = admin_client.post(news_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_initial == set(Comment.objects.all())
