# Create your tests here.
import json
from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from libnav.models import UserProfile, Floor
from django.test import TestCase, Client, RequestFactory


class APItests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        Floor.objects.create(number=1, mapName='')
        self.test_user = User.objects.create(username="testuser", password="warinbasingse")
        UserProfile.objects.get_or_create(user=self.test_user)
        self.test_user2 = User.objects.create(username="testuser2", email="email@website.com", password="mycabbages")
        UserProfile.objects.get_or_create(user=self.test_user2)

        self.friend = User.objects.create(username="friend", email="email@website.com", password="myfriends")
        self.friend_profile = UserProfile.objects.create(user=self.friend)
        self.friend_profile.friends.add(self.test_user)

    def test_set_point(self):
        data = dict()
        data['userID'] = self.test_user.id
        data['x'] = 500
        data['y'] = 450
        data['floor'] = 7
        data['private'] = False
        response = self.client.post(reverse('libnav:setloc'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_set_and_read_point_own(self):
        data = dict()
        data['userID'] = self.test_user.id
        data['x'] = 500
        data['y'] = 450
        data['floor'] = 7
        data['private'] = False
        response = self.client.post(reverse('libnav:setloc'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        query_data = {"userID": self.test_user.id, "floor": 7}
        points_response = self.client.get(reverse('libnav:getloc'), data=query_data)
        self.assertEqual(points_response.status_code, 200)

        self.assertEqual(points_response.content,
                         b'{"user_loc": [{"x": 500, "y": 450, "private": false, "name": "testuser"}], "friends": [], "others": []}')

    def test_set_and_read_point_others(self):
        data = dict()
        data['userID'] = self.test_user.id
        data['x'] = 500
        data['y'] = 450
        data['floor'] = 7
        data['private'] = False
        response = self.client.post(reverse('libnav:setloc'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        query_data = {"userID": self.test_user2.id, "floor": 7}
        points_response = self.client.get(reverse('libnav:getloc'), data=query_data)
        self.assertEqual(points_response.status_code, 200)

        self.assertEqual(points_response.content,
                         b'{"user_loc": [], "friends": [], "others": [{"x": 500, "y": 450}]}')

    def test_set_and_read_point_friends(self):
        data = dict()
        data['userID'] = self.test_user.id
        data['x'] = 500
        data['y'] = 450
        data['floor'] = 7
        data['private'] = False
        response = self.client.post(reverse('libnav:setloc'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        query_data = {"userID": self.friend.id, "floor": 7}
        points_response = self.client.get(reverse('libnav:getloc'), data=query_data)
        self.assertEqual(points_response.status_code, 200)

        self.assertEqual(points_response.content,
                         b'{"user_loc": [], "friends": [{"x": 500, "y": 450, "private": false, "name": "testuser"}], "others": []}')

    def test_unkown_user(self):
        with self.assertRaises(Exception):
            data = dict()
            data['userID'] = 99
            data['x'] = 500
            data['y'] = 450
            data['floor'] = 7
            data['private'] = False
            response = self.client.post(reverse('libnav:setloc'), data=json.dumps(data),
                                        content_type='application/json')
