"""Test case for models."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):
    """Create a question to be use in test."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    """Tests for Model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_already_ended_question(self):
        """is_published() returns True for questions whose end_date is already pass."""
        time = timezone.now() - datetime.timedelta(days=5)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.is_published(), True)

    def test_is_published_with_not_yet_published_question(self):
        """is_published() returns False for questions whose pub_date is not yet pass."""
        time = timezone.now() + datetime.timedelta(days=10)
        question = Question(pub_date=time)
        self.assertEqual(question.is_published(), False)

    def test_is_published_with_already_published_question(self):
        """is_published() returns True for questions that had already published."""
        time = timezone.now() - datetime.timedelta(days=5)
        question = Question(pub_date=time)
        self.assertEqual(question.is_published(), True)

    def test_can_vote_with_ended_question(self):
        """can_vote() returns False for questions whose end_date is already pass."""
        time = timezone.now() - datetime.timedelta(days=5)
        old_question = Question(end_date=time)
        self.assertEqual(old_question.can_vote(), False)

    def test_can_vote_with_not_ended_question(self):
        """can_vote() returns True for questions whose end_date is not yet pass."""
        time = timezone.now() + datetime.timedelta(days=10)
        question = Question(pub_date=time - datetime.timedelta(days=10), end_date=time)
        self.assertEqual(question.can_vote(), True)

    def test_can_vote_with_not_yet_published_question(self):
        """can_vote() returns False for questions that had not published yet."""
        time = timezone.now() + datetime.timedelta(days=10)
        question = Question(pub_date=time)
        self.assertEqual(question.can_vote(), False)
