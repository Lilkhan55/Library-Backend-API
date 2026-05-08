from rest_framework import serializers

from library.models import Book, Genre, TagPost

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_title(self, title):
        value = title.strip()

        if len(value) < 2:
            raise serializers.ValidationError('Слишком короткое название')
        return value
    
    def validate_counts(self, counts):
        if counts < 1:
            raise serializers.ValidationError('Количество должно быть больше 0')
        return counts
    
    def validate_data(self, attrs):
        if attrs['title'] == attrs['author']:
            raise serializers.ValidationError('Одинаковые название у полей title и author')
        return attrs

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = ['tag']

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = '__all__'
