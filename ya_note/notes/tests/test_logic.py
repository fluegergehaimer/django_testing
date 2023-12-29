"""Модуль проверки логики приложения."""
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .core import (
    Creation, NOTES_ADD_URL, NOTE_SUCCESS,
    NOTES_EDIT_URL, ADD_REDIRECT_URL,
    NOTES_DELETE_URL)


class TestNoteCreation(Creation):
    """Проверка создания заметок."""

    def test_user_can_create_note(self):
        """Авторизированный пользователь может создавать заметки."""
        note_count_initial = Note.objects.count()
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTE_SUCCESS)
        self.assertEqual(Note.objects.count(), note_count_initial + 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создавать заметки."""
        comments_count_initial = Note.objects.count()
        response = self.client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, ADD_REDIRECT_URL)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, comments_count_initial)


class TestLogic(Creation):
    """Проверка логики."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_count_initial = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertFormError(response, form='form',
                             field='slug', errors=self.note.slug + WARNING)
        self.assertEqual(Note.objects.count(), note_count_initial)

    def test_auto_slug(self):
        """Автоматически формируется slug."""
        note_count_initial = Note.objects.count()
        self.form_data.pop('slug')
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTE_SUCCESS)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, note_count_initial + 1)
        new_note = Note.objects.exclude(id=self.note.id).get()
        slugify_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, slugify_slug)


class TestCommentCreation(Creation):
    """Тест создания комментариев."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_anonymous_user_cant_delete_note(self):
        """Не авторизованный пользователь не может удалять заметки."""
        notes_count_initial = Note.objects.count()
        response = self.reader_client.post(
            NOTES_EDIT_URL,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_initial)

    def test_author_can_delete_note(self):
        """Пользователь может удалить свои заметки."""
        notes_count_initial = Note.objects.count()
        response = self.author_client.delete(NOTES_DELETE_URL)
        self.assertRedirects(response, NOTE_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count_initial - 1)

    def test_author_can_edit_note(self):
        """Пользователь может править свои заметки."""
        self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author, self.form_data['author'])

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может править чужие заметки."""
        response = self.reader_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
