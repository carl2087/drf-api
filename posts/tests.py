from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):

    # create a dummy user for test
    def setUp(self):
        User.objects.create_user(username='carl', password='12345')

    def test_can_list_posts(self):
        # grabbing the user from above
        carl = User.objects.get(username='carl')
        # attaching the user to the post
        Post.objects.create(owner=carl, title='a title')
        # saving the get request to a variable 'response'
        response = self.client.get('/posts/')
        # what we expect to be returned from the get request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print the response to the console
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        # login first with the created user
        self.client.login(username='carl', password='12345')
        # attach the post request to a variable
        response = self.client.post('/posts/', {'title': 'a title'})
        # counting the posts and saving to a variable
        count = Post.objects.count()
        # testing the return count on the posts is one
        self.assertEqual(count, 1)
        # testing the response of the created post is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        # attach the posts request to a variable
        response = self.client.post('/posts/', {'title': 'a title'})
        # testing the response is correct as no user logged in
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
