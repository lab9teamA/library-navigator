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

    floors = [
        {"number": 1, "mapname": "level1alpha.png"},
        {"number": 2, "mapname": "level2alpha.png"},
        {"number": 3, "mapname": "level3alpha.png"},
        {"number": 4, "mapname": "level4alpha.png"},
        {"number": 5, "mapname": "level5alpha.png"},
        {"number": 6, "mapname": "level6alpha.png"},
        {"number": 7, "mapname": "level7alpha.png"},
        {"number": 8, "mapname": "level8alpha.png"},
        {"number": 9, "mapname": "level9alpha.png"},
        {"number": 10, "mapname": "level10alpha.png"},
        {"number": 11, "mapname": "level11alpha.png"},
        {"number": 12, "mapname": "level12alpha.png"},
    ]
    bookcases = [
        {"id": "abc-ddd-lll", "floor":1},
        {"id": "abc-ddd-kkk", "floor":1},
        {"id": "abc-ddd-ccc", "floor":1},
        {"id": "bbb-ddd-lll", "floor":2},
        {"id": "bbb-ddd-kkk", "floor":2},
        {"id": "ggg-ddd-ccc", "floor":3},
        {"id": "hhh-ddd-ccc", "floor":4},
        {"id": "hbb-ddd-ccc", "floor":5},
        {"id": "hbb-ddd-cck", "floor":6},
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
    for floor in floors:
        f = Floor.objects.get_or_create(number = floor["number"], mapName=floor["mapname"])[0]
        f.save()
    for bookcase in bookcases:
        floor = Floor.objects.get(number = bookcase["floor"])
        b = Bookcase.objects.get_or_create(id = bookcase["id"], floor = floor)[0]
        b.save()
    for book in books:
        bc = Bookcase.objects.get(id=book["location"])
        c = Book.objects.get_or_create(ISBN=book["ISBN"],
                                       title=book["title"],
                                       author=book["author"],
                                       numberOfPage=book["numberOfPage"],
                                       likes=book["likes"],
                                       bookcase=bc,
                                       publishDate=book['publishDate']
                                       )[0]
        c.save()
        print(c,"-- added")



if __name__ == "__main__":
    populate()