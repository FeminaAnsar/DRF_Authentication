from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError('Users should have a Username')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=400,null=False)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.title
# Create your models here.
