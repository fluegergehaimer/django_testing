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


class ClientNoteCreation(TestCase):
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
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'slug',
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

    def note_creation(self, form, expected_slug):
        """Базовый метод создания заметок."""
        Note.objects.all().delete()
        response = self.author_client.post(NOTES_ADD_URL, form)
        self.assertRedirects(response, NOTE_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, expected_slug)
