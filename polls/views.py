"""Views for index page, detail page, and result page."""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class IndexView(generic.ListView):
    """View for detail page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Get the query set of question."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """View for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        """If question does not exist or can't be vote, redirect to index page."""
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
        """Get the query set of question."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class ResultsView(generic.DetailView):
    """View for result page."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Submit the vote for the poll."""
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
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
