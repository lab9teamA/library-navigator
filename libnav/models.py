# Create your models here.
from django.db import models


class Subject(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    name = models.CharField(max_length=50)


class Location(models.Model):
    floor = models.IntegerField()
    bookCaseID = models.CharField(max_length=10)


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    coverImage = models.ImageField()
    checkedOut = models.IntegerField()
    checkedOut = models.DateField()
    numberOfPage = models.IntegerField()
    description = models.CharField(max_length=1000)
    likes = models.IntegerField()
    location = models.ForeignKey(Location , on_delete=models.PROTECT)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    # TODO password = 1
    picture = models.ImageField()
    isReading = models.ManyToManyField(Book,related_name="user_isReading")
    recommends = models.ManyToManyField(Book,related_name="user_recommends")
