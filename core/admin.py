from django.contrib import admin
from .models import QuestionMix,Answer,Question
from django.contrib.admin import TabularInline, StackedInline


class AnswerInline(TabularInline):
    model = Answer
    extra = 0

class QuestionInline(StackedInline):
    model = Question
    extra = 0

class QuestionMixAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,AnswerInline,)

    class Meta:
        model = QuestionMix


admin.site.register(QuestionMix,QuestionMixAdmin)