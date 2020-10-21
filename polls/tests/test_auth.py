"""Test case for authentication."""
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):
    """Create a question to be use in test."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class AuthenticationTests(TestCase):
    """Tests for DetailView."""

    def test_authenticate_user(self):
        """Test if the user already login."""

        User = get_user_model()
        user = User.objects.create_user("John", "john@gmail.com", "12345")
        user.first_name = 'John'
        user.last_name = "Davidson"
        user.save()
        self.client.login(username="John", password="12345")
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "John")
        self.assertContains(response, "Davidson")

    def test_unauthenticate_user(self):
        """Test if the user does not login."""

        User = get_user_model()
        user = User.objects.create_user("John", "john@gmail.com", "12345")
        user.first_name = 'John'
        user.last_name = "Davidson"
        user.save()
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertNotContains(response, "John")
        self.assertNotContains(response, "Davidson")
