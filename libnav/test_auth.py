from django.test import TestCase, Client, RequestFactory
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth import authenticate
from django.urls import reverse

from libnav.models import User, UserProfile, Floor
from libnav.views import user_login

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        Floor.objects.create(number=1, mapName='')
        test_user = User.objects.create(username="testuser", password="warinbasingse")
        UserProfile.objects.get_or_create(user=test_user)
        merchant = User.objects.create(username="testuser2", email="email@website.com", password="mycabbages")
        UserProfile.objects.get_or_create(user=merchant)
        
    # check whether accounts can be created
    def test_register(self):
    
        # set up data to send through the register form
        data = {}
        data['submit'] = 'Register'
        data['username'] = 'newuser'
        data['password'] = 'bobross'
        
        # send request 
        response = self.client.post(reverse('libnav:login'), data)
        response.client = self.client
        self.assertRedirects(response, reverse('libnav:profile', kwargs={'username': 'newuser'}))
        
        # check email field 
        test_user = User.objects.get(username="newuser")
        self.assertEqual(test_user.email, '')
      
    # test to ensure you can't create account with an existing username
    def test_existing_account(self):
        self.assertRaises(IntegrityError, User.objects.create, username="testuser", password="newpassword")
        
    # check whether default image is present
    def test_profile_picture(self):
        test_user = User.objects.get(username="testuser")
        self.assertEqual(test_user.userprofile.picture.url, settings.MEDIA_URL+"profile_images/NONE.jpg")
    
    # email is present
    def test_email(self):
        test_user = User.objects.get(username="testuser")
        other_user = User.objects.get(username="testuser2")
        self.assertEqual(test_user.email, '')
        self.assertEqual(other_user.email, 'email@website.com')
    
    # can't log in with disabled account 
    def test_active_account(self):
        # disable account
        test_user = User.objects.get(username="testuser")
        test_user.is_active = False
        test_user.save()
        
        # set up data to send through the login form
        data = {}
        data['submit'] = 'Login'
        data['username'] = 'testuser'
        data['password'] = 'warinbasingse'
        
        # check whether response says that the account is disabled
        response = self.client.post(reverse('libnav:login'), data)
        self.assertContains(response, "Your LIBNAV account is disabled.")
        
        # re-enable account
        test_user.is_active = True
        test_user.save()
    
    # can't log in with wrong password 
    def test_password(self):
        # set up data to send through the login form
        data = {}
        data['submit'] = 'Login'
        data['username'] = 'testuser'
        data['password'] = 'warinbasignse'
        
        # send request 
        response = self.client.post(reverse('libnav:login'), data)
        self.assertContains(response, "Invalid login details supplied.")
        
    # if user already logged in, test whether it redirects to the profile page
    def test_profile_page_redirect(self):
        # log user in
        test_user = User.objects.get(username="testuser")
        self.client.login(username='testuser', password='warinbasingse')
        
        # check whether response redirects to profile page
        request = self.factory.get(reverse('libnav:login'), {'user': test_user})
        request.user = test_user
        response = user_login(request)
        response.client = self.client
        self.assertRedirects(response, reverse('libnav:profile', kwargs={'username': 'testuser'}))