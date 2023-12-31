"""Модуль с общими данными для тестов."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'Note'

LOGIN_URL = reverse('users:login')
NOTES_DETAIL_URL = reverse('notes:detail', args=(SLUG,))
NOTES_EDIT_URL = reverse('notes:edit', args=(SLUG,))
NOTES_DELETE_URL = reverse('notes:delete', args=(SLUG,))
HOMEPAGE_URL = reverse('notes:home')
SIGNUP_URL = reverse('users:signup')
LOGOUT_URL = reverse('users:logout')
NOTE_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTE_SUCCESS = reverse('notes:success')
ADD_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_ADD_URL}'
SUCCESS_REDIRECT_URL = f'{LOGIN_URL}?next={NOTE_SUCCESS}'
LIST_REDIRECT_URL = f'{LOGIN_URL}?next={NOTE_LIST_URL}'
DETAIL_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_DETAIL_URL}'
EDIT_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_EDIT_URL}'
DELETE_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_DELETE_URL}'


class Creation(TestCase):
    """Базовый класс для тестов."""

    @classmethod
    def setUpTestData(cls, note_creation=False, note_list_creation=False):
        """Создание данных на уровне класса."""
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': SLUG,
        }
        if note_creation:
            cls.note = Note.objects.create(
                title='Заголовок',
                text='Текст',
                author=cls.author,
                slug=SLUG
            )
        if note_list_creation:
            Note.objects.bulk_create(
                Note(
                    title=f'Заголовок {index}',
                    text='Текст',
                    author=cls.author,
                    slug=f'{SLUG}-{index}'
                )
                for index in range(10)
            )
