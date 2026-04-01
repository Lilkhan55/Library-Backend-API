from django.urls import path, re_path, register_converter
from . import views
from . import converters
from django.views.decorators.cache import cache_page

register_converter(converters.FourDigitYearConverter, "year4")

app_name = "libs"
urlpatterns = [
    path("", cache_page(30)(views.HomePage.as_view()), name="main"),
    path("about/", views.About.as_view(), name="about"),
    path("all/", views.AllBooks.as_view(), name="all"),
    path("contact/", views.GetContact.as_view(), name="contact"),
    path("book/<slug:slug>/", views.ShowBook.as_view(), name="book"),
    path("book/<slug:slug>/loan", views.BorrowBook.as_view(), name="loan"),
    path("book/<int:id>/return", views.ReturnBook.as_view(), name="return_loan"),
    path("genre/<slug:slug>/", views.BookGenre.as_view(), name="genre"),
    path("tag/<slug:slug>/", views.TagList.as_view(), name="tag"),
    path("add_book/", views.AddBook.as_view(), name="add_books"),
    path("edit/<slug:slug>/", views.UpdateBook.as_view(), name="edit"),
]
