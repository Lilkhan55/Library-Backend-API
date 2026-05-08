from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from library.models import Book, Genre, TagPost
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class BookAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class BookAPIList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = BookAPIListPagination

class BookAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, )

class BookAPIDelete(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
