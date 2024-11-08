"""Модуль проверки контента приложения."""
from http import HTTPStatus

from notes.forms import NoteForm
from .core import (
    ClientNoteCreation, NOTES_ADD_URL,
    NOTES_EDIT_URL, NOTE_LIST_URL
)


class SingleNoteTests(ClientNoteCreation):
    """Проверки отображения."""

    @classmethod
    def setUpTestData(cls):
        """Переопределение данных класса."""
        super().setUpTestData(note_creation=True)

    def test_client_cant_see_others_notes(self):
        """Неавторизованный пользователь не может видеть заметки."""
        response = self.reader_client.get(NOTE_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_author_client_note_list_display(self):
        """Авторизованый пользователь может видеть свои  заметки."""
        response = self.author_client.get(NOTE_LIST_URL)
        note = response.context['object_list'].get(pk=self.note.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_authorized_client_has_form(self):
        """Проверка формы авторизованного пользователя."""
        for url in (NOTES_ADD_URL, NOTES_EDIT_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
