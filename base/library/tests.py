import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Book, Genre, TagPost
 
User = get_user_model()

# Fixtures

@pytest.fixture
def api_client():
    return APIClient()
 
 
@pytest.fixture
def moderator(db):
    user = User.objects.create_user(
        username='moderator',
        password='testpass123',
        is_staff=True
    )
    return user
 
 
@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username='user',
        password='testpass123'
    )
 
 
@pytest.fixture
def auth_moderator(api_client, moderator):
    api_client.force_authenticate(user=moderator)
    return api_client
 
 
@pytest.fixture
def auth_user(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client
 
 
@pytest.fixture
def genre(db):
    return Genre.objects.create(name='Фантастика')
 
 
@pytest.fixture
def tag(db):
    return TagPost.objects.create(tag='Классика')
 
 
@pytest.fixture
def book(db, genre, moderator):
    return Book.objects.create(
        title='Тестовая книга',
        author='Тестовый автор',
        genre=genre,
        counts=5,
        description='Тестовое описание',
        user=moderator
    )

# Genre API tests

@pytest.mark.django_db
class TestGenreAPI:
 
    def test_get_genre_list(self, api_client, genre):
        response = api_client.get('/api/v1/genre/')
        assert response.status_code == status.HTTP_200_OK
 
    def test_create_genre_as_moderator(self, auth_moderator):
        data = {'name': 'Роман'}
        response = auth_moderator.post('/api/v1/genre/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Genre.objects.filter(name='Роман').exists()
 
    def test_create_genre_as_regular_user(self, auth_user):
        data = {'name': 'Детектив'}
        response = auth_user.post('/api/v1/genre/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
 
    def test_create_genre_unauthenticated(self, api_client):
        data = {'name': 'Поэзия'}
        response = api_client.post('/api/v1/genre/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
 
    def test_delete_genre_as_moderator(self, auth_moderator, genre):
        response = auth_moderator.delete(f'/api/v1/genre/{genre.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Genre.objects.filter(pk=genre.pk).exists()

# Book API tests

@pytest.mark.django_db
class TestBookAPI:
 
    def test_get_book_list(self, api_client, book):
        response = api_client.get('/api/v1/book/')
        assert response.status_code == status.HTTP_200_OK
 
    def test_get_book_detail(self, api_client, book):
        response = api_client.get(f'/api/v1/book/{book.pk}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Тестовая книга'
 
    def test_create_book_as_moderator(self, auth_moderator, genre, moderator):
        data = {
            'title': 'Новая книга',
            'author': 'Новый автор',
            'genre': genre.pk,
            'counts': 3,
            'description': 'Описание новой книги',
            'user': moderator.pk
        }
        response = auth_moderator.post('/api/v1/book/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(title='Новая книга').exists()
 
    def test_create_book_as_regular_user(self, auth_user, genre, regular_user):
        data = {
            'title': 'Книга юзера',
            'author': 'Автор',
            'genre': genre.pk,
            'counts': 1,
            'description': 'Описание',
            'user': regular_user.pk
        }
        response = auth_user.post('/api/v1/book/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
 
    def test_update_book_as_moderator(self, auth_moderator, book, genre, moderator):
        data = {
            'title': 'Обновлённая книга',
            'author': 'Тестовый автор',
            'genre': genre.pk,
            'counts': 10,
            'description': 'Новое описание',
            'user': moderator.pk
        }
        response = auth_moderator.put(f'/api/v1/book/{book.pk}/', data)
        assert response.status_code == status.HTTP_200_OK
        book.refresh_from_db()
        assert book.title == 'Обновлённая книга'
        assert book.counts == 10
 
    def test_partial_update_book(self, auth_moderator, book):
        response = auth_moderator.patch(f'/api/v1/book/{book.pk}/', {'counts': 99})
        assert response.status_code == status.HTTP_200_OK
        book.refresh_from_db()
        assert book.counts == 99
 
    def test_delete_book_as_moderator(self, auth_moderator, book):
        response = auth_moderator.delete(f'/api/v1/book/{book.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Book.objects.filter(pk=book.pk).exists()
 
    def test_delete_book_as_regular_user(self, auth_user, book):
        response = auth_user.delete(f'/api/v1/book/{book.pk}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
 
    def test_get_nonexistent_book(self, api_client):
        response = api_client.get('/api/v1/book/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

# Validation tests

@pytest.mark.django_db
class TestBookValidation:
 
    def test_short_title_validation(self, auth_moderator, genre, moderator):
        data = {
            'title': 'А',
            'author': 'Автор',
            'genre': genre.pk,
            'counts': 3,
            'description': 'Описание',
            'user': moderator.pk
        }
        response = auth_moderator.post('/api/v1/book/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data
 
    def test_negative_counts_validation(self, auth_moderator, genre, moderator):
        data = {
            'title': 'Нормальное название',
            'author': 'Автор',
            'genre': genre.pk,
            'counts': -1,
            'description': 'Описание',
            'user': moderator.pk
        }
        response = auth_moderator.post('/api/v1/book/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'counts' in response.data
 
    def test_book_with_tags(self, auth_moderator, genre, tag, moderator):
        data = {
            'title': 'Книга с тегами',
            'author': 'Автор',
            'genre': genre.pk,
            'counts': 5,
            'description': 'Описание',
            'tags': [tag.pk],
            'user': moderator.pk
        }
        response = auth_moderator.post('/api/v1/book/', data)
        assert response.status_code == status.HTTP_201_CREATED
        book = Book.objects.get(title='Книга с тегами')
        assert tag in book.tags.all()

# Filter tests

@pytest.mark.django_db
class TestBookFilters:
 
    def test_filter_by_author(self, api_client, book):
        response = api_client.get('/api/v1/book/?author=Тестовый автор')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
 
    def test_ordering_by_counts(self, api_client, book):
        response = api_client.get('/api/v1/book/?ordering=counts')
        assert response.status_code == status.HTTP_200_OK
 
    def test_ordering_by_title(self, api_client, book):
        response = api_client.get('/api/v1/book/?ordering=title')
        assert response.status_code == status.HTTP_200_OK
