import tablib
from import_export.fields import Field
from import_export.resources import ModelResource
from django.conf import settings
from parler.utils.context import switch_language


class TranslatableModelResource(ModelResource):
    def export(self, queryset=None, *args, **kwargs):
        """
        Exports a resource.
        """

        self.before_export(queryset, *args, **kwargs)

        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)

        for obj in self.iter_queryset(queryset):
            for language in obj.get_available_languages():
                with switch_language(obj, language):
                    data.append(self.export_resource(obj))

        # This is useful for a generalized version

        # for obj in self.iter_queryset(queryset):
        #     try:
        #         for language in obj.get_available_languages():
        #             with switch_language(obj, language):
        #                 data.append(self.export_resource(obj))
        #     except AttributeError:
        #         data.append(self.export_resource(obj))

        self.after_export(queryset, data, *args, **kwargs)

        return data


class LangField(Field):
    def save(self, obj, data, is_m2m=False, **kwargs):
        language = data['language_code'] or settings.PARLER_DEFAULT_LANGUAGE_CODE
        attrs = self.attribute.split('__')
        cleaned = self.clean(data, **kwargs)
        obj.set_current_language(language)
        setattr(obj, attrs[-1], cleaned)
