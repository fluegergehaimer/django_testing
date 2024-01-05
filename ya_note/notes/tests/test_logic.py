"""Модуль проверки логики приложения."""
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .core import (
    ClientNoteCreation, NOTES_ADD_URL, NOTE_SUCCESS,
    NOTES_EDIT_URL, ADD_REDIRECT_URL, NOTES_DELETE_URL
)


class TestNoteCreation(ClientNoteCreation):
    """Проверка создания заметок."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_anonym_cant_create_note(self):
        """Анонимный пользователь не может создавать заметки."""
        notes = set(Note.objects.all())
        response = self.client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, ADD_REDIRECT_URL)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        notes = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD_URL, data=self.form_data)
        self.assertFormError(response, form='form',
                             field='slug', errors=self.note.slug + WARNING)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_user_can_create_note_with_and_without_slug(self):
        """Пользователь может создавать заметки со слагом и без."""
        cases = [
            ('', slugify(self.form_data['title'])),
            ('slug', self.form_data['slug'])
        ]
        for slug, expected_slug in cases:
            self.form_data['slug'] = slug
            Note.objects.all().delete()
            response = self.author_client.post(NOTES_ADD_URL, self.form_data)
            self.assertRedirects(response, NOTE_SUCCESS)
            self.assertEqual(Note.objects.count(), 1)
            note = Note.objects.get()
            self.assertEqual(note.title, self.form_data['title'])
            self.assertEqual(note.text, self.form_data['text'])
            self.assertEqual(note.author, self.author)
            self.assertEqual(note.slug, expected_slug)
        else:
            print('Тест пройден без ошибок.')

    def test_anonym_client_cant_delete_note(self):
        """Не авторизованный пользователь не может удалять заметки."""
        notes = set(Note.objects.all())
        response = self.reader_client.post(
            NOTES_EDIT_URL,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(set(Note.objects.all()), notes)

    def test_author_can_delete_note(self):
        """Пользователь может удалить свои заметки."""
        notes_count = Note.objects.count()
        response = self.author_client.delete(NOTES_DELETE_URL)
        self.assertRedirects(response, NOTE_SUCCESS)
        self.assertEqual(Note.objects.count(), notes_count - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_author_can_edit_note(self):
        """Пользователь может править свои заметки."""
        self.author_client.post(NOTES_EDIT_URL, data=self.form_data)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может править чужие заметки."""
        response = self.reader_client.post(NOTES_EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
