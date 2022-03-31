from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from .models import Student, StudentTopicStatus, StudentTopicMastery


class StudentFilter(AutocompleteFilter):
    title = 'Student'
    field_name = 'student'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'create_timestamp',
    )
    search_fields = ['user__username']


@admin.register(StudentTopicStatus)
class StudentTopicStatus(admin.ModelAdmin):
    search_fields = [
        'topic__translations__name',
        'student__user__username',
    ]
    list_filter = (
        'student',
        'topic__area_of_knowledge__universal_area_knowledge',
    )
    list_display = (
        'id',
        'update_timestamp',
        'student',
        'topic',
        'status',
    )


@admin.register(StudentTopicMastery)
class StudentTopicMastery(admin.ModelAdmin):
    search_fields = [
        'topic__translations__name',
        'student__user__username',
    ]
    list_filter = (
        'student',
        'topic__area_of_knowledge__universal_area_knowledge',
    )
    list_display = (
        'id',
        'update_timestamp',
        'student',
        'topic',
        'mastery_level',
        'status',
    )
