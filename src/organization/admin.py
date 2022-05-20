from django.contrib import admin
from .models.org import Organization, OrganizationPersonnel
from .models.schools import Group, School, SchoolPersonnel, AdministrativePersonnel, Teacher, Classroom


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of', 'slug', 'parent')
    search_fields = ('name', 'parent',)
    list_filter = ('type_of', 'slug', 'student_plan',)


@admin.register(OrganizationPersonnel)
class OrganizationPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number', 'position')
    search_fields = ('user', 'organization', 'name', 'last_name',)
    list_filter = ('position', 'gender',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'internal_code', 'population', 'slug',
                    'grade', 'school_personnel')
    search_fields = ('name', 'internal_code', 'school_personnel',)
    list_filter = ('area_of_knowledges', 'grade', 'slug', 'population',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'internal_code', 'type_of', 'organization')
    search_fields = ('name', 'internal_code', 'organization',)
    list_filter = ('student_plan', 'type_of', 'slug',)


@admin.register(SchoolPersonnel)
class SchoolPersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('user', 'school', 'name', 'last_name', 'identification_number',
                     'position', 'zip', 'country', 'district',)
    list_filter = ('position', 'gender', 'gender', 'identification_number',)


@admin.register(AdministrativePersonnel)
class AdministrativePersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('user', 'school', 'name', 'last_name', 'identification_number',
                     'position', 'zip', 'country', 'district',)
    list_filter = ('position', 'gender', 'gender', 'identification_number',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school', 'discountCode', 'name', 'last_name',
                    'gender', 'date_of_birth', 'identification_number',
                    'position', 'zip', 'country', 'district')
    search_fields = ('user', 'school', 'name', 'last_name', 'identification_number',
                     'position', 'zip', 'country', 'district',)
    list_filter = ('position', 'gender', 'gender', 'identification_number',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'audience', 'school', 'teacher', 'enable_games', 'game_cost', 'time_zone',
                    'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                    'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
                    'sunday_start', 'sunday_end')
    search_fields = ('name', 'audience', 'school', 'teacher',)
    list_filter = ('language', 'audience', 'school', 'game_cost', 'time_zone',)
