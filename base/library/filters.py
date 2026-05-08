import django_filters
from .models import Book, Genre, TagPost

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')
    counts = django_filters.RangeFilter()
    class Meta:
        model = Book
        fields = {
            'author': ['icontains'],
        }

    def filter_title(self, queryset, name, value):
        value = value.split(' ')
        return queryset.filter(title__icontains=''.join(value).lower())
    
class GenreFilter(django_filters.FilterSet):
    class Meta:
        model = Genre
        fields = {
            'name': ['icontains']
        }

class TagFilter(django_filters.FilterSet):
    class Meta:
        model = TagPost
        fields = {
            'tag': ['icontains']
        }
