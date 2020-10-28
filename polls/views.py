"""Views for index page, detail page, and result page."""
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Choice, Vote
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.auth.models import User
import logging

log = logging.getLogger("polls")
logging.basicConfig(level=logging.INFO)


def get_client_ip(request):
    """Get the client's ip address."""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def update_choice_login(request, **kwargs):
    """Update your last vote when login."""
    for question in Question.objects.all():
        question.last_vote = str(request.user.vote_set.get(question=question).selected_choice)
        question.save()


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log when user login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Login user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log when user logout."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Logout user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log when user fail to login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.warning('Login user(failed): %s , IP: %s , Date: %s', credentials['username'], ip, str(date))


class IndexView(generic.ListView):
    """View for detail page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Get the queryset of question.

        :return question's queryset.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """View for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        """
        If question does not exist or can't be vote, redirect to index page.

        :param request is the HttpRequest object.
        :param *args is the argument.
        :param **kwargs is the keyword argument.
        :return redirect to index page if the question can't be vote or does not exist,
                redirect to the question page otherwise.
        """
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote():
                error = "You can't vote on this poll because this poll is already ended."
                return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
        except ObjectDoesNotExist:
            error = "Poll does not exist."
            return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
        self.object = self.get_object()
        context = self.get_context_data(object=self.get_object())
        template_name = 'polls/detail.html'
        return render(request, context=context, template_name=template_name)

    def get_queryset(self):
        """
        Get the queryset of question.

        :return question's queryset.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ResultsView(generic.DetailView):
    """View for result page."""

    model = Question
    template_name = 'polls/results.html'


@login_required()
def vote(request, question_id):
    """
    Submit the vote for the poll.

    :param request is the HttpRequest object.
    :param question_id is the id of the question.
    :return redirect to index page if question can't be voted,
            redirect to the same page with an error message if the choice is not selected,
            redirect to the results page otherwise.
    """
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        error = "You can't vote on this poll because this poll is already ended."
        return HttpResponseRedirect(reverse('polls:index'), messages.error(request, error))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'selected_choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(selected_choice=choice).count()
            choice.save()
        for question in Question.objects.all():
            question.last_vote = str(request.user.vote_set.get(question=question).selected_choice)
            question.save()
        date = datetime.now()
        log = logging.getLogger("polls")
        log.info("User: %s, Poll's ID: %d, Date: %s.", user, question_id, str(date))
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
