from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# CustomUser model extends the AbstractUser model to include additional fields (accessLevel, team, and department)
class CustomUser(AbstractUser):
    accessLevel = models.IntegerField(db_column='accessLevel', default=1)
    team = models.ForeignKey('Team', models.SET_NULL, db_column='teamID', blank=True, null=True)
    department = models.ForeignKey('Department', models.SET_NULL, db_column='departmentID', blank=True, null=True)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username

# Department model represents a department in the organisation
class Department(models.Model):
    departmentID = models.AutoField(db_column='departmentID', primary_key=True) 
    departmentName = models.CharField(db_column='departmentName', max_length=100)  
    departmentLeaderID = models.IntegerField(db_column='departmentLeaderID')  

    class Meta:
        db_table = 'Department'

    def __str__(self):
        return self.departmentName

# Team model represents a team within a department
class Team(models.Model):
    team = models.AutoField(db_column='teamID', primary_key=True)  
    department = models.ForeignKey(Department, models.DO_NOTHING, db_column='departmentID', default=0)  
    teamName = models.CharField(db_column='teamName', max_length=100) 
    teamLeaderID = models.IntegerField(db_column='teamLeaderID') 

    def __str__(self):
        return self.teamName

    class Meta:
        db_table = 'Team'

# Employee model represents an employee in the organisation
class Employee(models.Model):
    employeeID = models.AutoField(db_column='employeeID', primary_key=True) 
    team = models.ForeignKey('Team', models.DO_NOTHING, db_column='teamID', blank=True, null=True)  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(db_column='firstName', max_length=100)  
    lastName = models.CharField(db_column='lastName', max_length=100)  
    jobTitle = models.CharField(db_column='jobTitle', max_length=100)  

    class Meta:
        db_table = 'Employee'

    def __str__(self):
        return self.firstName + " " + self.lastName