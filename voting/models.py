#Authored by Nate
from django.db import models
from accounts.models import Employee

# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100)
    green_desc = models.CharField(max_length=300)
    amber_desc = models.CharField(max_length=300)
    red_desc = models.CharField(max_length=300)

    class Meta:
        db_table = 'Question'

    def __str__(self):
        return self.question_title
    
class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    survey_title = models.CharField(max_length=100)
    survey_description = models.CharField(max_length=300)
    survey_type = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, through='SurveyDetail', related_name='surveys')

    class Meta:
        db_table = 'Survey'

    def __str__(self):
        return self.survey_title

class SurveyResponse(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # in prod, change to protect
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) # in prod, change to protect
    session = models.ForeignKey('Session', on_delete=models.CASCADE) # in prod, change to protect

    class Meta:
        db_table = 'SurveyResponse'
        unique_together = (('employee', 'session'),)

    def __str__(self):
        return f"Response in session {self.session} by {self.employee.firstName} {self.employee.lastName}"
    
class SurveyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SurveyDetail'
        unique_together = ('survey', 'question')

    def __str__(self):
        return f"{self.survey.survey_title} - {self.question.question_title}"  

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) # in prod, change to protect
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = 'Session'

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.survey.survey_title} ({self.start_date.date()} - {self.end_date.date()})"

class SurveyResponseDetail(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE)
    # answer choices for survey response
    GREEN = 'green'
    AMBER = 'amber'
    RED = 'red'
    answer_choices = [
        (GREEN, 'Green'),
        (AMBER, 'Amber'),
        (RED, 'Red'),
    ]
    answer = models.CharField(choices=answer_choices , max_length=10)
    # improvement state choices for survey response
    STABLE = 'stable'
    IMPROVING = 'improving'
    GETTING_WORSE = 'getting worse'
    improvement_choices = [
        (STABLE, 'Stable'),
        (IMPROVING, 'Improving'),
        (GETTING_WORSE, 'Getting Worse'),
    ]
    improvement_state = models.CharField(choices=improvement_choices, max_length=20)
    
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'SurveyResponseDetail'
    def __str__(self):
        return f"Detail {self.id} for Response {self.response.id} on Question {self.question.question_title}"