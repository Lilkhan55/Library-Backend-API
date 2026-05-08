
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.utils import timezone

from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from library.models import Book, Genre, TagPost, UploadFiles, BorrowRecords
from .utils import DataMixin
from .serializers import BookSerializer, GenreSerializer, TagSerializer
from .permissions import ModeratorOrReadOnly
from .filters import BookFilter, GenreFilter, TagFilter

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [ModeratorOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = BookFilter
    ordering_fields = ['id', 'title', 'author', 'counts']

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ModeratorOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = GenreFilter
    ordering_fields = ['id', 'name']
    
class TagViewSet(ModelViewSet):
    queryset = TagPost.objects.all()
    serializer_class = TagSerializer
    permission_classes = [ModeratorOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TagFilter
    ordering_fields = ['id', 'name']
        

class BorrowBookViewSet(APIView):
    def post(self, request, id):
        book_obj = get_object_or_404(Book, id=id)

        active_loan = BorrowRecords.objects.filter(user=request.user, books=book_obj, returned_at__isnull=True).exists

        if active_loan:
            return Response(status='400', data={'book':'Книга уже занята'})
        
        if book_obj != 0:
            book_obj.counts -= 1
            book_obj.save()

            BorrowRecords.objects.create(user=request.user, books=book_obj, borrowed_at=timezone.now(), borrowed_due=timezone.now() + timezone.timedelta(days=14))

        return Response(status=status.HTTP_201_CREATED, data={'book':f'Книга {book_obj} была назначена пользователю {request.user}'})
    
class ReturnBook(APIView):
    def post(self, request, id):
        borrow_book = get_object_or_404(BorrowRecords, id=id, user=request.user, returned_at__isnull=True)
        borrow_book.books.counts += 1
        borrow_book.books.save()

        borrow_book.returned_at = timezone.now()
        borrow_book.is_returnded = True
        borrow_book.save()

        return Response(status=status.HTTP_202_ACCEPTED, data={'book':f'Книга {borrow_book.books.title} успешно возвращена'})

        
