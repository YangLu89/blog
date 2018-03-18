# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from views import index, view_post
from models import Blogpost
from datetime import datetime


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertIn(b'<title>Welcome to my blog</title>', response.content)

    def test_blogpost_create_with_show_in_homepage(self):
        Blogpost.objects.create(title='hello', author='admin', slug='this_is_a_test', body='This is a blog', posted=datetime.now)
        response = self.client.get('/')
        self.assertIn(b'This is a blog', response.content)


class BlogpostTest(TestCase):
    def test_blogpost_create_with_view(self):
        Blogpost.objects.create(title='hello', author='admin', slug='this_is_a_test', body='This is a blog', posted=datetime.now)
        response = self.client.get('/blog/this_is_a_test.html')
        self.assertIn(b'This is a blog', response.content)

    def test_blogpost_url_resolves_to_blog_post_view(self):
        found = resolve('/blog/this_is_a_test.html')
        self.assertEqual(found.func, view_post)


from django.test import LiveServerTestCase
from selenium import webdriver


class HomepageTestCase(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome('/Users/yang/Work/yang/chromedriver')
        self.selenium.maximize_window()
        super(HomepageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomepageTestCase, self).tearDown()

    def test_visit_homepage(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/')
        )

        self.assertIn('Welcome to my blog', self.selenium.title)


class BlogpostFromHomepageCase(LiveServerTestCase):
    def setUp(self):
        Blogpost.objects.create(
            title = 'hello',
            author = 'admin',
            slug = 'this_is_a_test',
            body = 'This is a blog',
            posted = datetime.now
        )

        self.selenium = webdriver.Chrome('/Users/yang/Work/yang/chromedriver')
        self.selenium.maximize_window()
        super(BlogpostFromHomepageCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(BlogpostFromHomepageCase, self).tearDown()

    def test_visit_blog_post(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, '/')
        )

        self.selenium.find_element_by_link_text('hello').click()
        self.assertIn('hello', self.selenium.title)
