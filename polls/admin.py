"""Administration site."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    """Register choice into a question.."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Register a new question."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('End Date information', {'fields': ['end_date'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.site_url = 'http://127.0.0.1:8000/polls/'
admin.site.register(Question, QuestionAdmin)
