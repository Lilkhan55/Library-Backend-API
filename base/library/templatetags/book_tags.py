from django import template
from library.models import Book, Genre, TagPost
from django.db.models import Count
from library.utils import menu


register = template.Library()

@register.simple_tag
def get_menu():
    return menu
     
@register.inclusion_tag('library/include/list_genre.html')
def show_genres():
    g = Genre.objects.annotate(num_books=Count("page")).filter(num_books__gt=0)
    return {'genres': g}

@register.inclusion_tag('library/include/list_tags.html')
def show_tags():
    t = TagPost.objects.annotate(num_tags=Count("tags")).filter(num_tags__gt=0)
    return {'tags' : t}
