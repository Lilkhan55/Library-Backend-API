from django.urls import path, include
from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'book', viewset=views.BookViewSet)
router.register(r'genre', viewset=views.GenreViewSet)
router.register(r'tag', viewset=views.TagViewSet)

app_name = 'library'

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
