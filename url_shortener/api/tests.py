from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Link

class LinkTests(APITestCase):

    def setUp(self):
        # Создаем администратора и обычного пользователя
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.normal_user = User.objects.create_user(username='user', password='userpass')

        # Получаем токены для авторизации
        response = self.client.post('http://127.0.0.1:8000/api/auth/token/login/', {'username': 'admin', 'password': 'adminpass'})
        self.admin_token = response.data['auth_token']

        response = self.client.post('http://127.0.0.1:8000/api/auth/token/login/', {'username': 'user', 'password': 'userpass'})
        self.user_token = response.data['auth_token']

        # Устанавливаем заголовки авторизации для клиента
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        self.normal_client = self.client.__class__()
        self.normal_client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')

    def test_create_link(self):
        """
        Проверяет, что обычные пользователи могут создавать новые ссылки
        """
        url = 'http://example.com'
        response = self.normal_client.post('http://127.0.0.1:8000/api/links/', {'url': url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)
        self.assertEqual(Link.objects.get().url, url)

    def test_admin_can_delete_link(self):
        """
        Проверяет, что администратор может удалять ссылки
        """
        link = Link.objects.create(url='http://example.com', user=self.normal_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')
        response = self.client.delete(f'http://127.0.0.1:8000/api/links/{link.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Link.objects.count(), 0)

    def test_user_cannot_delete_link(self):
        """
        Проверяет, что обычный пользователь не может удалять ссылки
        """
        link = Link.objects.create(url='http://example.com', user=self.normal_user)
        response = self.normal_client.delete(f'http://127.0.0.1:8000/api/links/{link.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Link.objects.count(), 1)

    def test_view_link_list(self):
        """
        Проверяет, что все пользователи могут просматривать список ссылок
        """
        Link.objects.create(url='http://example.com', user=self.normal_user)
        response = self.normal_client.get('http://127.0.0.1:8000/api/links/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_view_user_links(self):
        """
        Проверяет, что можно получить список пользователей и созданных ими ссылок
        """
        Link.objects.create(url='http://example.com', user=self.normal_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token}')
        response = self.client.get('http://127.0.0.1:8000/api/user-links/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data[0])
        self.assertIn('links', response.data[0])

    def test_admin_can_delete_user_and_links(self):
        """
        Проверяет, что при удалении пользователя удаляются все ссылки пользователя
        """
        link = Link.objects.create(url='http://example.com', user=self.normal_user)
        # Удаляем пользователя напрямую из базы данных
        User.objects.filter(pk=self.normal_user.pk).delete()
        self.assertEqual(Link.objects.count(), 0)

    # def test_redirect_to_original_url(self):
    #     """
    #     Проверяет, что перенаправление по короткому URL происходит на оригинальный URL
    #     """
    #     original_url = 'http://vk.com'
    #     link = Link.objects.create(url=original_url, user=self.normal_user)
    #     response = self.client.get(f'http://127.0.0.1:8000/api/redirect/{link.short_url}/')
    #     self.assertEqual(response.status_code, status.HTTP_302_FOUND)
    #     self.assertEqual(response['Location'], original_url)

    # def test_click_increment(self):
    #     """
    #     Проверяет, что количество кликов увеличивается при переходе по короткому URL
    #     """
    #     original_url = 'http://vk.com'
    #     link = Link.objects.create(url=original_url, user=self.normal_user)
    #     self.client.get(f'http://127.0.0.1:8000/api/redirect/{link.short_url}/')
    #     link.refresh_from_db()
    #     self.assertEqual(link.clicks, 1)
