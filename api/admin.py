from django.contrib import admin

from .models import Job_title, Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'middle_name', 'Job_title', 'hired', 'salary')
    list_display_links = ('first_name', )
    search_fields = ('id', 'first_name', 'second_name', 'middle_name', 'Job_title', 'hired', 'salary', 'chief', 'username')
    list_filter = ('Job_title',)


class Job_titleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_editable = ('title',)
    search_fields = ('title',)
    ordering = ('id', 'title',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Job_title, Job_titleAdmin)