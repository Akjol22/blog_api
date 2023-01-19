from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from collections import OrderedDict

from .views import PostViewSet
from .models import Post, Category
from account.models import User


class PostTest(APITestCase):

    def SetUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(
            title='cat1'
        )
        user = User.objects.create_user(
            email='akzolkanaev81@gmail.com',
            password='1234',
            is_active=True,
            name='Akjol',
            last_name='Kanaev'
        )
        img = open('/home/akjol/Downloads/Telegram Desktop/photo_2021-12-30_14-47-32.jpg', 'rb')
        post = [
            Post(author=user, body='new post',
            title='post1', image=img, category=self.category, slug='1'),
        
            Post(author=user, body='new post',
            title='post1', image=img, category=self.category, slug='2'),

            Post(author=user, body='new post',
            title='post1', image=img, category=self.category, slug='3'),

            Post(author=user, body='new post',
            title='post1', image=img, category=self.category, slug='4')
        ]
        Post.obojects.bulk_create(post)

    def test_list(self):
        request = self.factory.get('posts/')
        view = PostViewSet.as_view({'get': 'list'})
        response = view(request)
        # print(response.data)

        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict

    def test_retrieve(self):
        slug = Post.objects.all()[0].slug
        request = self.factory.get(f'posts/{slug}/')
        view = PostViewSet.as_view({'get': 'retrive'})
        response = view(request, pk=slug)
        print(response.data)

        assert response.status_code == 200

    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'body': 'vava',
            'title': 'post4',
            'category': 'cat1'
        }
        request = self.factory.post('posts/', data, format='json')
        force_authenticate(request, user=user)
        view = PostViewSet.as_view({'post': 'create'})
        response = view(request)
        print(response.data)

        assert response.status_code == 201
        assert response.data['body'] == data['body']
        assert Post.objects.filter(author=user, body=data['body']).exists()

        # TODO: test_update, test_delete, test_forgot_password_complate