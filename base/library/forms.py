from django import forms
from . import models
from captcha.fields import CaptchaField


class AddBookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = [
            'title',
            'author',
            'genre',
            'description',
            'counts',
            'tags',
            'cover',
            'has_file'
            ]
        labels = {'description':'Описание', 'tags':'Тэги'}
    #title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class':'form-input'}))
    #author = forms.CharField(max_length=255, label='Автор')
    #slug = forms.SlugField(max_length=255, required=False, label='URL')
    #description = forms.CharField(widget=forms.Textarea(), required=False, label='Описание')
    #genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label='Жанр', empty_label='Не выбрано')
    #tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label='Теги')
    #counts = forms.IntegerField(label='Количество экземпляров')
    #cover = forms.ImageField(label='Обложка книги', required=False)

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Письмо', widget=forms.Textarea(attrs={'cols':60, 'rows':10}))
    captcha = CaptchaField()
