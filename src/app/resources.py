from import_export.fields import Field
from django.conf import settings


class LangField(Field):
    def save(self, obj, data, is_m2m):
        lang = data['language_code'] or settings.PARLER_DEFAULT_LANGUAGE_CODE
        obj.set_current_language(lang)
        super().save(obj, data, is_m2m)
