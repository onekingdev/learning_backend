from django.contrib import admin

from students.models import Student
from .models.org import Organization, OrganizationPersonnel
from .models.schools import Group, School, SchoolAdministrativePersonnel, SchoolPersonnel, AdministrativePersonnel, SchoolTeacher, SchoolSubscriber, Teacher, Classroom, TeacherClassroom

class SchoolTeacherInline(admin.StackedInline):
    model = SchoolTeacher
    extra = 0

class AssignSchoolToTeacherInline(admin.StackedInline):
    model = SchoolTeacher
    extra = 0
    verbose_name = "Assign School With Plan"
    verbose_name_plural = "Assign Schools With Plan"

class AssingClassroomToTeacherInline(admin.StackedInline):
    model = TeacherClassroom
    extra = 0
    verbose_name = "Assign Clasroom With Plan"
    verbose_name_plural = "Assign Clasrooms With Plan"

class AssignTeacherToClassroomInline(admin.StackedInline):
    model = TeacherClassroom
    extra = 0
    verbose_name = "Assign Teacher With Plan"
    verbose_name_plural = "Assign Teacher With Plan"

class SchoolSubscriberInline(admin.StackedInline):
    model = SchoolSubscriber
    extra = 0

class SchoolAdministrativePersonnelInline(admin.StackedInline):
    model = SchoolAdministrativePersonnel
    extra = 0

class StudentInline(admin.StackedInline):
    model = Student

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

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of',)
    search_fields = ('id', 'name',)
    list_filter = ('type_of', 'is_active', 'create_timestamp', 'update_timestamp')
    inlines = [
        SchoolTeacherInline,
        SchoolSubscriberInline,
        SchoolAdministrativePersonnelInline,
    ]

@admin.register(SchoolTeacher)
class SchoolTeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'teacher')
    search_fields = ('id', 'school', 'teacher')
    list_filter = ('is_active', 'create_timestamp', 'update_timestamp')

@admin.register(SchoolPersonnel)
class SchoolPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name',
                    'gender')
    search_fields = ('id', 'user__username', 'last_name',
                     )
    list_filter = ('gender',)


@admin.register(AdministrativePersonnel)
class AdministrativePersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name',
                    'gender')
    search_fields = ('id', 'user__username', 'last_name',
                    )
    list_filter = ('gender', 'is_active', 'create_timestamp', 'update_timestamp')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_name',
                    'gender', 
                    )
    search_fields = ('id', 'user__username', 'name', 'last_name',
                     'position', )
    list_filter = ('gender', 
                   'is_active', 'create_timestamp', 'update_timestamp')
    inlines = [
        AssignSchoolToTeacherInline,
        AssingClassroomToTeacherInline,
    ]

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'audience', 'enable_games', 'game_cost_percentage', 'time_zone_value',
                    'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                    'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
                    'sunday_start', 'sunday_end')
    search_fields = ('id', 'name', 'audience__translations__name',
                     'school__name', 'teacher__name', 'teacher__last_name')
    list_filter = ('grade', 'language', 'audience', 'game_cost_percentage',
                   'time_zone_value', 'is_active', 'create_timestamp', 'update_timestamp')

    inlines = [AssignTeacherToClassroomInline]
