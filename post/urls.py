from django.urls import path, include
from .views import CategoryListView, TagListView, PostViewSet, CommentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('tags/', TagListView.as_view()),
    path('', include(router.urls)),
]