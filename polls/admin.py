from django.db import models
from django.contrib import admin
from utils import widgets
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text','pub_date_fa']
    formfield_overrides = {models.DateField:{'widget':widgets.PersianDateTimeWidget}}
