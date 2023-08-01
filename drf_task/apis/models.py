from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

# User Model
class User(AbstractBaseUser):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=55, null=False)
    password = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=100, null=False, unique=True)


    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')

    def __str__(self):
        return self.title
    

class Article(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title
    





