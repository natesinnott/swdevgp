#Authored by Eeliya
from django.db import models
# department model, maps to Department table
class Department(models.Model):
    departmentid = models.AutoField(db_column='departmentID', primary_key=True)
    departmentname = models.CharField(db_column='departmentName', max_length=100)
    departmentleaderid = models.IntegerField(db_column='departmentLeaderID')

    class Meta:
        managed = False
        db_table = 'Department'


# employee model, links to user and team
class Employee(models.Model):
    employeeid = models.AutoField(db_column='employeeID', primary_key=True)
    firstname = models.CharField(db_column='firstName', max_length=100)
    lastname = models.CharField(db_column='lastName', max_length=100)
    jobtitle = models.CharField(db_column='jobTitle', max_length=100)
    # one-to-one link to user
    user = models.OneToOneField('User', models.DO_NOTHING, blank=True, null=True)
    # fk to team
    teamid = models.ForeignKey('Team', models.DO_NOTHING, db_column='teamID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee'


# model for survey question with descs for each color
class Question(models.Model):
    question_title = models.CharField(max_length=100)
    green_desc = models.CharField(max_length=300)
    amber_desc = models.CharField(max_length=300)
    red_desc = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'Question'


# session model, links to a survey
class Session(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # fk to survey
    survey = models.ForeignKey('Survey', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Session'


# model for survey metadata
class Survey(models.Model):
    survey_title = models.CharField(max_length=100)
    survey_description = models.CharField(max_length=300)
    survey_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Survey'


# links specific question to a survey
class Surveydetail(models.Model):
    question = models.ForeignKey(Question, models.DO_NOTHING)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SurveyDetail'
        unique_together = (('survey', 'question'),)


# stores an employee's response for a survey session
class Surveyresponse(models.Model):
    # fk to employee who submitted
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)
    # fk to session this response belongs to
    session = models.ForeignKey(Session, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SurveyResponse'
        unique_together = (('employee', 'session'),)


# stores answers to individual questions in a response
class Surveyresponsedetail(models.Model):
    answer = models.CharField(max_length=10)
    improvement_state = models.CharField(max_length=20)
    comment = models.TextField(blank=True, null=True)
    # fk to the question answered
    question = models.ForeignKey(Question, models.DO_NOTHING)
    # fk to related survey response
    response = models.ForeignKey(Surveyresponse, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SurveyResponseDetail'


# team model, linked to department
class Team(models.Model):
    teamid = models.AutoField(db_column='teamID', primary_key=True)
    teamname = models.CharField(db_column='teamName', max_length=100)
    teamleaderid = models.IntegerField(db_column='teamLeaderID')
    # fk to department
    departmentid = models.ForeignKey(Department, models.DO_NOTHING, db_column='departmentID')

    class Meta:
        managed = False
        db_table = 'Team'


# custom user model with team and department access
class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    accesslevel = models.IntegerField(db_column='accessLevel')
    # fk to department
    departmentid = models.ForeignKey(Department, models.DO_NOTHING, db_column='departmentID', blank=True, null=True)
    # fk to team
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'