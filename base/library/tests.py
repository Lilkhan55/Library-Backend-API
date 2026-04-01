from django.test import TestCase
from django.urls import reverse

from library.models import Book

class GetBookTestCase(TestCase):
    fixtures = ['library_book.json', 'library_genre.json', 'library_tags.json']
    def setUp(self):
        "Инициализация"

    def test_mainpage(self):
        path = reverse('libs:main')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
       
    def test_data_mainpage(self):
        b = Book.instock.select_related('genre')
        path = reverse('libs:main')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context['object_list'], b)

    def test_paginate_allpage(self):
        path = reverse('libs:all')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f"?page={page}")
        b = Book.objects.all().select_related('genre')
        self.assertQuerySetEqual(response.context['object_list'], b[(page-1) * paginate_by:page * paginate_by])

    def tearDown(self):
        "Завершение"
