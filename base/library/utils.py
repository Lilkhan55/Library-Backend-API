menu = [
    {'title':'Главная страница', 'url_name':'libs:main'},
    {'title':'О сайте', 'url_name':'libs:about'},
    {'title':'Список книг', 'url_name':'libs:all'},
    {'title':'Обратная связь', 'url_name':'libs:contact'},  
    {'title':'Добавить книгу', 'url_name': 'libs:add_books'},
]

class DataMixin:
    paginate_by = 5
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context
