from django.contrib import admin
from .models import Question, Answer
from django.conf import settings


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['poll_title', 'is_active']}
         ),
        ('Информация о дате',
         {'fields': ['date_published'],
          'classes': ['collapse']}
         ),
    ]
    inlines = [AnswerInline]

    search_fields = ['title']


    list_display = ('poll_title', 'date_published', 'is_active')
    list_filter = ['date_published']


admin.site.register(Question, QuestionAdmin)