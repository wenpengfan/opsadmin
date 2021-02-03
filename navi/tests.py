#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client


# Create your tests here.
class NaviTest(TestCase):
    def test_index(self):
        self.client = Client(enforce_csrf_checks=True)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
