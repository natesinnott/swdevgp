from django.db import models
from accounts import Employee

# Create your models here.


class Question(models.Model):
    questionID = models.IntegerField(db_column='questionID', unique='True', blank='False')
    questionTitle = models.CharField(db_column='questionTitle', max_length=100)
    greenDesc = models.CharField(db_column='greenDescription', max_length=300)
    amberDesc = models.CharField(db_column='amberDescription', max_length=300)
    redDesc = models.CharField(db_column='redDescription', max_length=300)

    class Meta:
        db_table = 'Question'

    def __str__(self):
        return self.questionTitle
    
class Survey(models.Model):
    surveyID = models.IntegerField(db_column='surveyID')
    surveyTitle = models.CharField(db_column='surveyTitle', max_length=100)
    surveyDescription = models.CharField(db_column='surveyDescription', max_length=300)
    surveyType = models.CharField(db_column='surveyType', max_length=100)

    class Meta:
        db_table = 'Survey'

    def __str__(self):
        return self.surveyTitle

class Response(models.Model):
    responseID = models.IntegerField(db_column='responseID')
    employeeID = models.ForeignKey(Employee, models.DO_NOTHING, db_column='employeeID')
    surveyID = models.ForeignKey(Survey, models.DO_NOTHING, db_column='surveyID')
    quarter = models.IntegerField(db_column='quarter')
    year = models.IntegerField(db_column='year')

    class Meta:
        db_table = 'Response'

    def __str__(self):
        return self.responseID
    
class surveyDetail(models.Model):
    surveyDetailID = models.IntegerField(db_column='surveyDetailID', serialize='True')
    surveyID = models.ForeignKey(Survey, models.DO_NOTHING, db_column='surveyID')
    questionID = models.ForeignKey(Question, models.DO_NOTHING, db_column='questionID')

    class Meta:
        db_table = 'surveyDetail'

    def __str__(self):
        return self.surveyDetailID
    

class responseDetail(models.Model):
    responseDetailID = models.IntegerField(db_column='responseDetailID', serialize='True')
    questionID = models.ForeignKey(Question, models.DO_NOTHING, db_column='questionID')
    responseID = models.ForeignKey(Response, models.DO_NOTHING, db_column='responseID')
    answer = models.CharField(db_column='answer', max_length=10)
    improvementState = models.IntegerField(db_column='improvementState')
    comment = models.CharField(db_column='comment', max_length=1000)