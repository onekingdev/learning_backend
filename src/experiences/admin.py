from django.contrib import admin
from .models import Level
from parler import admin as parler_admin

# Register your models here.
@admin.register(Level)
class LevelAdmin(parler_admin.TranslatableAdmin):
    pass
