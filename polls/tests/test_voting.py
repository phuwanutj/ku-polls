"""Test case for DetailView."""
import datetime
import os
import itertools
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.conf import settings
from importlib import import_module
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Choice


def create_question(question_text, days):
    """Create a question to be use in test."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class VotingTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user("John", "john@gmail.com", "12345")
        user.first_name = 'John'
        user.last_name = "Davidson"
        user.save()

    def test_unauthenticate_vote(self):
        question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 302)

    def test_authenticate_vote(self):
        self.client.login(username="John", password="12345")
        question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
