from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from rest_framework import routers

from . import views
from .routers import MyRouter
#from .views import BookViewSet

#router = MyRouter()
#router.register(r'book', BookViewSet, basename='book')

#app_name = 'api'
#urlpatterns = [
    #path('v1/', include(router.urls)),
    #path('v1/bookdetail/', views.BookAPIList.as_view(), name='booklist'),
    #path('v1/bookupdate/<int:pk>/', views.BookAPIUpdate.as_view(), name='bookupdate'),
    #path('v1/bookdelete/<int:pk>/', views.BookAPIDelete.as_view(), name='bookdelete'),
#]
