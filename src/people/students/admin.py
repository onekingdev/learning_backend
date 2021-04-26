from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Student


# Register your models here.
@admin.register(Student)
class StudentAdmin(DraggableMPTTAdmin):
    pass
