import string

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
                  ]
        
    def validate_username(self, username):
        if string.punctuation in username or string.whitespace in username:
            raise serializers.ValidationError('Недопустимые символы')
        
        if len(username) < 2:
            raise serializers.ValidationError('Слишком короткий ник')
        
        return username
    
    def validate_email(self, email):
        if '@' not in email:
            raise serializers.ValidationError('Неверный формат email')
        
        if len(email) < 9:
            raise serializers.ValidationError('Слишком короткий email')
        return email
        
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
            password = validated_data.pop("password1")
            validated_data.pop("password2")

            user = User.objects.create_user(
                password=password, **validated_data)
            return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'is_superuser',
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            'date_joined',
            'photo',
            'groups',
        ]
        
        