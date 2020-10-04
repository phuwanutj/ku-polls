"""Question and Choice for polls app."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A question for voting."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("date ended", default=None, null=True)

    def __str__(self):
        """Return question's text."""
        return self.question_text

    def was_published_recently(self):
        """Check whether this poll was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check whether this poll is published."""
        now = timezone.now()
        if self.pub_date <= now:
            return True
        return False

    def can_vote(self):
        """Check whether user can vote on this poll."""
        now = timezone.now()
        if (self.end_date is None or now <= self.end_date) and self.is_published():
            return True
        return False


class Choice(models.Model):
    """A choice for a question's answer."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice's text."""
        return self.choice_text
