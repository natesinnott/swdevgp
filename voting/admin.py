from django.contrib import admin
from .models import Question, Survey, SurveyResponse, SurveyDetail, SurveyResponseDetail, Session

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_title', 'green_desc', 'amber_desc', 'red_desc')
    search_fields = ('question_title',)
    list_per_page = 10

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey_title', 'survey_type')
    search_fields = ('survey_title',)
    # This will allow you to filter the surveys by type
    list_filter = ('survey_type',)

@admin.register(SurveyDetail)
class SurveyDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question')
    search_fields = ('survey__survey_title', 'question__question_title')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'start_date', 'end_date', 'is_active')
    search_fields = ('survey__survey_title',)
    list_filter = ('start_date', 'end_date')

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'survey', 'session')
    search_fields = ('employee__first_name', 'employee__last_name', 'survey__survey_title')
    list_filter = ('session',)

@admin.register(SurveyResponseDetail)
class SurveyResponseDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'response', 'question', 'answer', 'improvement_state')
    search_fields = ('question__question_title', 'response__id')
    list_filter = ('answer', 'improvement_state')