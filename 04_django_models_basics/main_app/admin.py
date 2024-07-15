from django.contrib import admin

from main_app.models import Employee, Department, Project

# Register your models here.

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Project)
