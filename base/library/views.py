import random
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import first, last
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, FormView
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.utils import timezone

from library.models import Book, Genre, TagPost, UploadFiles, BorrowRecords
from .forms import AddBookForm, UploadFileForm, ContactForm
from .utils import DataMixin
from library.main import counter
from pytils.translit import slugify

class HomePage(DataMixin, ListView):
    context_object_name = 'books'
    template_name = 'library/main.html'
    title_page = 'Главная страница'
    
    def get_queryset(self):
        return (Book.instock.select_related('genre').order_by('?')[:3])
    
class About(DataMixin, TemplateView):
    template_name = 'library/about.html'
    title_page = 'Страница о нас'

class ShowBook(DataMixin, DetailView):
    template_name = 'library/single_book.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'book'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title= context['book'].title)
    
    def get_object(self, queryset = None):
        return get_object_or_404(Book.instock, slug = self.kwargs[self.slug_url_kwarg])

class BookGenre(DataMixin, ListView):
    template_name = 'library/main.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.instock.filter(genre__slug = self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context['books'][0].genre
        return self.get_mixin_context(context, 
                                      title_page = 'Категория: ' + genre.name)

class TagList(DataMixin, ListView):
    template_name = 'library/main.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.instock.filter(tags__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['slug'])
        return self.get_mixin_context(context, title= 'Тэг: ' + tag.tag)

class AddBook(PermissionRequiredMixin,LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm # связана с моделью Book
    title_page = 'Добавление книги'
    template_name = 'library/addpage.html'
    success_url = reverse_lazy('libs:main')
    extra_context = {'title':'Добавить книгу'}
    permission_required = 'library.add_book'

class UpdateBook(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Book
    form_class = AddBookForm
    template_name = 'library/addpage.html'
    title_page = 'Обновление книги'
    success_url = reverse_lazy('libs:main')
    extra_context = {'title':'Изменить книгу'}
    permission_required = 'library.change_book'

    def form_valid(self, form):
        try:
            form.save()
            return super().form_valid(form)
        except IntegrityError:
            pass


#def all_books(request):
#    books = Book.instock.filter().order_by('id')
#    data = {
#        'title':'Список всех книг',
#        'menu': menu,
#        'books': books,
#    }
#    return render(request, 'library/main.html', context=data)

class AllBooks(DataMixin, ListView):
    template_name = 'library/main.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        b_lst = cache.get('book_posts')
        if not b_lst:
            b_lst = Book.instock.filter().order_by('id')
            cache.set('book_posts', b_lst, 60)
        return b_lst
    

class GetContact(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'library/contact.html'
    success_url = reverse_lazy('libs:main')
    extra_context = {'title':'Связаться с нами'}

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>\n<p>Нужный ресурс не был найден на этом сервере</p>')

class BorrowBook(LoginRequiredMixin, DataMixin, View):
    success_url = reverse_lazy('users:profile')
    def post(self, request, slug):
        book_obj = get_object_or_404(Book, slug=slug)

        active_loan = BorrowRecords.objects.filter(user=request.user, books=book_obj, returned_at__isnull=True).exists()
        
        if active_loan:
            return redirect('libs:main')
            
        if book_obj.counts != 0:
            book_obj.counts -= 1
            book_obj.save()

            BorrowRecords.objects.create(user=request.user, books=book_obj, borrowed_at=timezone.now(), borrowed_due=timezone.now() + timezone.timedelta(days=14))

        return redirect(self.success_url)
    
class ReturnBook(LoginRequiredMixin, DataMixin, View):
    success_url = reverse_lazy('users:profile')
    def post(self, request, id):
        borrow_book = get_object_or_404(BorrowRecords, id=id, user=request.user, returned_at__isnull=True)
        borrow_book.books.counts += 1
        borrow_book.books.save()
        
        borrow_book.returned_at = timezone.now()
        borrow_book.is_returnded = True
        borrow_book.save()
        return redirect(self.success_url)
        
