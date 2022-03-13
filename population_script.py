import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_navigator.settings')

import django
from random import randint

django.setup()

from libnav.models import *


def populate():
    subjects = [
        {"name": "Philosophy"},
        {"name": "Maths"},
        {"name": "Engineering"},
        {"name": "Computing Science"},
        {"name": "Anime"},
        {"name": "Romance"},
    ]

    locations = [
        {"floor": 1, "bookCaseID": "abc-ddd-lll"},
        {"floor": 1, "bookCaseID": "abc-ddd-kkk"},
        {"floor": 1, "bookCaseID": "abc-ddd-ccc"},
        {"floor": 2, "bookCaseID": "bbb-ddd-lll"},
        {"floor": 2, "bookCaseID": "bbb-ddd-kkk"},
        {"floor": 3, "bookCaseID": "ggg-ddd-ccc"},
        {"floor": 4, "bookCaseID": "hhh-ddd-ccc"},
        {"floor": 5, "bookCaseID": "hbb-ddd-ccc"},
        {"floor": 6, "bookCaseID": "hbb-ddd-cck"},
    ]

    books = [
        {"ISBN": "9780393354324",
         "title": "Guns, Germs, and Steel",
         "author": "Jared Diamond",
        "numberOfPage": 123,
        "likes" : random.randint(0,212),
         "location":"abc-ddd-lll",
         'publishDate':'2001-01-01',
         },
        {"ISBN": "9780393223324",
         "title": "Head First Java",
         "author": "Bert Bates",
        "numberOfPage": 123,
        "likes" : random.randint(0,212),
         "location":"hbb-ddd-cck",
         'publishDate': '2001-01-01',

         },
    ]

    for sub in subjects:
        s = Subject.objects.get_or_create(name=sub["name"])[0]
        s.save()
    for loc in locations:
        loc = Location.objects.get_or_create(floor=loc["floor"],bookCaseID=loc["bookCaseID"])[0]
        loc.save()
    for book in books:
        loc = Location.objects.get(bookCaseID=book["location"])
        c = Book.objects.get_or_create(ISBN=book["ISBN"],
                                       title=book["title"],
                                       author=book["author"],
                                       numberOfPage=book["numberOfPage"],
                                       likes=book["likes"],
                                       location=loc,
                                       publishDate=book['publishDate']
                                       )[0]
        c.save()
        print(c,"-- added")



if __name__ == "__main__":
    populate()