import io

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from library.models import Book

class BookModel:
    def __init__(self, title, author, genre, counts, description, tags):
        self.title = title
        self.author = author
        self.genre = genre
        self.counts = counts
        self.description = description
        self.tags = tags

class BookSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'counts', 'description', 'tags', 'user']

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        book = Book.objects.create(**validated_data)

        if tags:
            book.tags.set(tags)

        return book
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)

        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.counts = validated_data.get('counts', instance.counts)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance
