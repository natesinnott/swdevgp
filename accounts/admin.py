from django.contrib import admin
from .models import CustomUser, Department, Team, Employee

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'accessLevel')
    search_fields = ('username', 'email')
    list_per_page = 10
    ordering = ('id',)
    list_filter = ('accessLevel',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentID', 'departmentName', 'departmentLeaderID')
    search_fields = ('departmentName',)
    list_per_page = 10
    ordering = ('departmentID',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'department', 'teamName', 'teamLeaderID')
    search_fields = ('teamName',)
    list_per_page = 10
    ordering = ('team',)
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeID', 'firstName', 'lastName', 'jobTitle', 'team')
    search_fields = ('firstName', 'lastName')
    list_per_page = 10
    ordering = ('employeeID',)
    list_filter = ('team',)