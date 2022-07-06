from django.contrib import admin
from .models.org import Organization, OrganizationPersonnel
from .models.schools import Group, School, SchoolPersonnel, AdministrativePersonnel, SchoolTeacher, SubscriberSchool, Teacher, Classroom


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of', 'slug', 'parent')
    search_fields = ('id', 'name', 'slug')
    list_filter = ('type_of', 'slug', 'student_plan', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(OrganizationPersonnel)
class OrganizationPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number', 'position')
    search_fields = ('id', 'user__username', 'organization__name', 'name', 'last_name', 'identification_number')
    list_filter = ('organization', 'position', 'gender', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',
                     )
    list_filter = (
                   'is_active', 'create_timestamp', 'update_timestamp')


class SchoolTeacherInline(admin.TabularInline):
    model = SchoolTeacher

class SchoolSubscriberInline(admin.TabularInline):
    model = SubscriberSchool


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of',)
    search_fields = ('id', 'name',)
    list_filter = ('type_of', 'is_active', 'create_timestamp', 'update_timestamp')
    inlines = [
        SchoolTeacherInline,
        SchoolSubscriberInline,
    ]

@admin.register(SchoolTeacher)
class SchoolTeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'teacher')
    search_fields = ('id', 'school', 'teacher')
    list_filter = ('is_active', 'create_timestamp', 'update_timestamp')

@admin.register(SchoolPersonnel)
class SchoolPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'last_name',
                    'gender')
    search_fields = ('id', 'user__username', 'last_name',
                     )
    list_filter = ('school', 'gender')


@admin.register(AdministrativePersonnel)
class AdministrativePersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'last_name',
                    'gender')
    search_fields = ('id', 'user__username', 'school__name', 'last_name',
                    )
    list_filter = ('gender', 'school__name', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'last_name',
                    'gender', 
                    )
    search_fields = ('id', 'user__username', 'name', 'last_name',
                     'position', )
    list_filter = ('school', 'gender', 
                   'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'audience', 'enable_games', 'game_cost', 'time_zone',
                    'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                    'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
                    'sunday_start', 'sunday_end')
    search_fields = ('id', 'name', 'audience__translations__name',
                     'school__name', 'teacher__name', 'teacher__last_name')
    list_filter = ('grade', 'language', 'audience', 'game_cost',
                   'time_zone', 'is_active', 'create_timestamp', 'update_timestamp')
