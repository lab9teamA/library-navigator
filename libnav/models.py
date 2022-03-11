# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    floor = models.IntegerField()
    bookCaseID = models.CharField(max_length=10)

    def __str__(self):
        return  str(self.bookCaseID) +" at "+str(self.floor)




class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    coverImage = models.ImageField()
    checkedOut = models.DateTimeField()
    publishDate = models.DateField()
    numberOfPage = models.IntegerField()
    description = models.CharField(max_length=1000)
    likes = models.IntegerField()
    location = models.ForeignKey(Location , on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_images",blank=True)
    isReading = models.ManyToManyField(Book,related_name="user_isReading")
    recommends = models.ManyToManyField(Book,related_name="user_recommends")

    def __str__(self):
        return self.user.username