from django.db import models

from django.core.validators import MinValueValidator
from django.urls import reverse

from pytils.translit import slugify

from users.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя жанра')
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Жанры"
        verbose_name_plural = "Жанры"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("libs:genre", kwargs={"slug": self.slug})
    

class InstockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(counts__gt=0)
        
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, default='Неизвестен', verbose_name='Автор')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='page', verbose_name='Жанр')
    description = models.TextField(default='Описание отсутствует')
    counts = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Количество')
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    cover = models.ImageField(upload_to='сovers', default=None, blank=True, null=True, verbose_name='Обложка')
    has_file = models.FileField(upload_to='files', default=None, blank=True, null=True, verbose_name='Файл')
    user = models.ForeignKey(User, verbose_name='Пользователь', default=1, on_delete=models.SET_DEFAULT)

    objects = models.Manager()
    instock = InstockManager()

    def save(self, *args, **kwargs):
        if not self.slug:  # slug создаётся только при пустом значении
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.author}"

    class Meta:
        verbose_name = "Книги"
        verbose_name_plural = "Книги"
        ordering = ["-counts"]
        indexes = [models.Index(fields=["title","author"])]

    def get_absolute_url(self):
        return reverse("libs:book", kwargs={"slug": self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse("libs:tag", kwargs={"slug": self.slug})
    
    class Meta:
        verbose_name = "Тэги"
        verbose_name_plural = "Тэги"

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')

class BorrowRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    borrowed_due = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    is_returnded = models.BooleanField(null=True, blank=True)
