from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .views import RegistrationView, LoginView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView, LogoutView


from .models import User


class UserTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='akzolkanaev81@gmail.com',
            password='1234',
            is_active=True
        )

    def test_register(self):
        data = {
            'email': 'akzolkanaev812@gmail.com',
            'password': '4567',
            'password_confirm': '4567',
            'name': 'Akjol',
            'last_name': 'Kanaev'
        }
        request = self.factory.post('register/', data, format='json')
        # print(request)
        view = RegistrationView.as_view()
        response = view(request)
        # print(response)
        
        assert response.status_code == 201
        assert User.objects.filter(email=data['email']).exists()

    def test_login(self):
        data = {
            'email': 'akzolkanaev81@gmail.com',
            'password': '1234'
        }
        request = self.factory.post('login/', data, format='json')
        view = LoginView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code == 200
        assert 'token' in response.data

    def test_change_password(self):
        data = {
            'old_password': '1234',
            'new_password': '4567',
            'new_password_confirm': '4567'
        }
        request = self.factory.post('change_password/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code == 200
        # assert data['new_password'] == data['new_password_confirm']

    def test_forgot_password(self):
        data = {
            'email': 'akzolkanaev81@gmail.com'
        }
        request = self.factory.post('forgot_password/', data, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        print(response)

        assert response.status_code == 200

    # def test_forgot_password_complate(self):
    #     data = {
    #         'code': '',
    #         'email': 'akzolkanaev81@gmail.com',
    #         'password': '4567',
    #         'password_confirm': '4567'
    #     }
    #     request = self.factory.post('forgot_password_complete/', data, format='json')
    #     view = ForgotPasswordCompleteView.as_view()
    #     response = view(request)
    #     print(response)

    #     assert response.status_code == 201


    def test_logout(self):
        force_authenticate(request, user=self.user)
        request = self.factory.post('logout/', format='json')
        view = LogoutView.as_view()
        response = view(request)
        print(response)

        assert response.status_code == 200