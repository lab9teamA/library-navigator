import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_navigator.settings')

import django

django.setup()

from libnav.models import *
from django.core.files import File


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
         "coverImage": "9780393354324.jpg",
         'publishDate': '2001-01-01',
         "numberOfPage": 123,
         "description": "Testosterone to the max",
         "likes": random.randint(0,212),
         "bookcase": "abc-ddd-lll",
         "subjects": ["Anime"],
         },
        {"ISBN": "9780393354325",
         "title": "Head First Java",
         "author": "Bert Bates",
         "coverImage": "9780393354325.jpg",
         'publishDate': '2001-01-01',
         "numberOfPage": 145,
         "description": "Waste your time with OO programming",
         "likes": random.randint(0, 212),
         "bookcase": "ggg-ddd-ccc",
         "subjects": ["Computing Science"],
         },
        {"ISBN": "9780393354326",
         "title": "Kama Sutra",
         "author": "Vātsyāyana",
         "coverImage": "9780393354326.jpg",
         'publishDate': '1882-01-01',
         "numberOfPage": 94,
         "description": "Shag",
         "likes": random.randint(0, 212),
         "bookcase": "bbb-ddd-lll",
         "subjects": ["Romance"],
         },
        {"ISBN": "9780393354327",
         "title": "A Brief History of Time",
         "author": "Stephen Hawking",
         "coverImage": "9780393354327.jpg",
         'publishDate': '1988-06-21',
         "numberOfPage": 312,
         "description": "Your mind = blown",
         "likes": random.randint(0, 212),
         "bookcase": "bbb-ddd-lll",
         "subjects": ["Philosophy", "Maths"],
         },
        {"ISBN": "9780393354328",
         "title": "Little Red Riding Hood",
         "author": "Bob Ross",
         "coverImage": "9780393354328.jpg",
         'publishDate': '1999-12-31',
         "numberOfPage": 15,
         "description": "Classic fairytale story",
         "likes": random.randint(0, 212),
         "bookcase": "bbb-ddd-lll",
         "subjects": ["Engineering"],
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
        bc = Bookcase.objects.get(id=book["bookcase"])
        c = Book.objects.get_or_create(ISBN=book["ISBN"],
                                       title=book["title"],
                                       author=book["author"],
                                       publishDate=book['publishDate'],
                                       numberOfPage=book["numberOfPage"],
                                       description=book['description'],
                                       likes=book["likes"],
                                       bookcase=bc,
                                       )[0]
        if book.get("coverImage") is not None:
        # media/coverImage can't have the same name or multiple copies of the image will be made
            c.coverImage.save(book["coverImage"], File(open("populationImages/" +book["coverImage"], "rb")))
        c.save()
        for subj in book["subjects"]:
            c.subjects.add(Subject.objects.get(name=subj))
        print(c,"-- added")



if __name__ == "__main__":
    populate()