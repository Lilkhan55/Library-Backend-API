import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
 
User = get_user_model()
 
# Fixtures

@pytest.fixture
def api_client():
    return APIClient()
 
 
@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        password='adminpass123',
        email='admin@test.com'
    )
 
 
@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username='regularuser',
        password='userpass123',
        email='user@test.com'
    )
 
 
@pytest.fixture
def auth_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client
 
 
@pytest.fixture
def auth_user(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client
 
# Registration tests
 
@pytest.mark.django_db
class TestRegisterAPI:
 
    def test_register_success(self, api_client):
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='newuser').exists()
 
    def test_register_passwords_mismatch(self, api_client):
        data = {
            'username': 'newuser2',
            'email': 'newuser2@test.com',
            'first_name': 'Петр',
            'last_name': 'Петров',
            'password1': 'strongpass123',
            'password2': 'wrongpass456',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data or 'non_field_errors' in response.data
 
    def test_register_short_username(self, api_client):
        data = {
            'username': 'a',
            'email': 'short@test.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
 
    def test_register_invalid_email(self, api_client):
        data = {
            'username': 'validuser',
            'email': 'bademail',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
 
    def test_register_short_email(self, api_client):
        data = {
            'username': 'validuser',
            'email': 'a@b.co',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
 
    def test_register_duplicate_username(self, api_client, regular_user):
        data = {
            'username': 'regularuser', 
            'email': 'another@test.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
 
    def test_register_password_not_returned(self, api_client):
        data = {
            'username': 'secureuser',
            'email': 'secure@test.com',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        }
        response = api_client.post('/users/api/v1/registration/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'password1' not in response.data
        assert 'password2' not in response.data
 
 

# JWT auth tests
 
@pytest.mark.django_db
class TestJWTAuth:
 
    def test_obtain_token(self, api_client, regular_user):
        data = {
            'username': 'regularuser',
            'password': 'userpass123',
        }
        response = api_client.post('/users/api/v1/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
 
    def test_obtain_token_wrong_password(self, api_client, regular_user):
        data = {
            'username': 'regularuser',
            'password': 'wrongpassword',
        }
        response = api_client.post('/users/api/v1/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
    def test_obtain_token_nonexistent_user(self, api_client):
        data = {
            'username': 'ghostuser',
            'password': 'somepass123',
        }
        response = api_client.post('/users/api/v1/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
    def test_refresh_token(self, api_client, regular_user):
        # Get ttoken
        login_data = {'username': 'regularuser', 'password': 'userpass123'}
        login_response = api_client.post('/users/api/v1/login/', login_data)
        refresh_token = login_response.data['refresh']
 
        # Refreshing token
        response = api_client.post('/users/api/v1/token/refresh/', {'refresh': refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
 
    def test_verify_token(self, api_client, regular_user):
        # Get token
        login_data = {'username': 'regularuser', 'password': 'userpass123'}
        login_response = api_client.post('/users/api/v1/login/', login_data)
        access_token = login_response.data['access']
 
        # Verification
        response = api_client.post('/users/api/v1/token/verify/', {'token': access_token})
        assert response.status_code == status.HTTP_200_OK
 
    def test_verify_invalid_token(self, api_client):
        response = api_client.post('/users/api/v1/token/verify/', {'token': 'invalidtoken'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
# User list tests
 
@pytest.mark.django_db
class TestUserListAPI:
 
    def test_userlist_as_admin(self, auth_admin, regular_user):
        response = auth_admin.get('/users/api/v1/userlist/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
 
    def test_userlist_as_regular_user(self, auth_user):
        response = auth_user.get('/users/api/v1/userlist/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
 
    def test_userlist_unauthenticated(self, api_client):
        response = api_client.get('/users/api/v1/userlist/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
 
    def test_userlist_contains_correct_fields(self, auth_admin, regular_user):
        response = auth_admin.get('/users/api/v1/userlist/')
        assert response.status_code == status.HTTP_200_OK
        user_data = response.data[0]
        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name']
        for field in expected_fields:
            assert field in user_data
 
