# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Floor(models.Model):
    number = models.IntegerField(primary_key=True)
    mapName = models.CharField( max_length= 20)
    def __str__(self):
        return "Floor "+ str(self.number)

class Bookcase(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT)

    def __str__(self):
        return  str(self.id) +" on "+str(self.floor)


class Book(models.Model):
    ISBN = models.CharField(max_length=13, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    coverImage = models.ImageField(upload_to='book_cover_images',null=True)
    checkedOut = models.BooleanField(default=False)
    numCheckedOut = models.IntegerField(default=0)
    publishDate = models.DateField()
    numberOfPage = models.IntegerField()
    description = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    bookcase = models.ForeignKey(Bookcase, on_delete=models.PROTECT)
    subjects = models.ManyToManyField(Subject,related_name='book_subjects',blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_images",blank=True,default="profile_images/NONE.jpg")
    website = models.URLField(blank= True)
    description = models.CharField(max_length = 1000, blank=True)
    isReading = models.ManyToManyField(Book,related_name="user_isReading",blank=True)
    recommends = models.ManyToManyField(Book,related_name="user_recommends",blank=True)
    likes = models.ManyToManyField(Book,related_name="user_likes",blank=True)
    friends = models.ManyToManyField(User,related_name='user_friends',blank=True)
    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name= 'from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)