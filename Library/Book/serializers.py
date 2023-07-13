from .models import User,Book
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model=User
        fields=['username','password']

class BookSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    class Meta:
        model=Book
        fields=['id','title','description','author','price']
