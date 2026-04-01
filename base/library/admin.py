from django.contrib import admin
from .models import Book, Genre, TagPost

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'author',
        'genre',
        'counts',
        'description',
        'tags',
        'slug',
        'cover',
        ]
    list_display = (
        'id',
        'title',
        'author',
        'genre',
        'counts',
        'status_info'
        )
    list_display_links = ('id', 'title')
    ordering = ['id', 'counts']
    list_editable = ('counts', )
    list_per_page = 8
    actions = ['set_status']
    search_fields = ['title', 'author', 'genre__name']
    list_filter = ('genre__name', 'tags')
    readonly_fields = ('slug',)

    @admin.display(description= 'Статус', ordering= 'counts')
    def status_info(self, book: Book):
        if book.counts > 0:
            return 'Доступна'
        else:
            return 'Нет в наличии'
    
    @admin.action(description='Изменить количество')
    def set_status(self, request, queryset):
        count_of_changes = queryset.update(counts=0)
        self.message_user(request, f'Изменено {count_of_changes} записей')
        
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['id', 'name']
    readonly_fields = ("slug",)

@admin.register(TagPost)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('tag', 'slug')
    ordering = ['id', 'tag']
    readonly_fields = ("slug",)
