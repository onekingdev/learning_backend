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
        #
        # for obj in self.iter_queryset(queryset):
        #     try:
        #         for language in obj.get_available_languages():
        #             with switch_language(obj, language):
        #                 data.append(self.export_resource(obj))
        #     except AttributeError:
        #         data.append(self.export_resource(obj))

        self.after_export(queryset, data, *args, **kwargs)

        return data

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for i in range(10):
            print()
        print('BEFORE IMPORT')
        print('Dataset:', dataset)
        print()

    def before_import_row(self, row, row_number=None, **kwargs):
        print('BEFORE IMPORT ROW')
        print('Row:', row)
        print()

    def after_import_instance(self, instance, new, row_number=None, **kwargs):
        print('AFTER IMPORT INSTANCE')
        print('Instance:', instance, 'New:', new)
        print('Dict:', instance.__dict__)
        print('Available languages:', instance.get_available_languages())
        print('Current language:', instance.get_current_language())
        print()

        # with switch_language(instance, )

    def before_save_instance(self, instance, using_transactions, dry_run):
        print('BEFORE SAVE INSTANCE')
        print('Instance:', instance)
        print('Available languages:', instance.get_available_languages())
        print('Current language:', instance.get_current_language)
        print('Current language:', instance._current_language)
        print()

    def after_save_instance(self, instance, using_transactions, dry_run):
        print('AFTER SAVE INSTANCE')
        print('Instance:', instance)
        print('Available languages:', instance.get_available_languages())
        print('Current language:', instance.get_current_language)
        print('Current language:', instance._current_language)
        print()

    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        print('AFTER IMPORT ROW')
        print('Row:', row)
        print()

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        print('AFTER IMPORT')
        print('Result:', result)
        print()


class LangField(Field):
    # def save(self, obj, data, is_m2m, *args, **kwargs):
    #     print('This is the save')
    #     lang = data['language_code'] or settings.PARLER_DEFAULT_LANGUAGE_CODE
    #     obj.set_current_language(lang)
    #     super().save(obj, data, is_m2m, *args, **kwargs)

    def save(self, obj, data, is_m2m=False, **kwargs):
        """
        If this field is not declared readonly, the object's attribute will
        be set to the value returned by :meth:`~import_export.fields.Field.clean`.
        """
        language = data['language_code'] or settings.PARLER_DEFAULT_LANGUAGE_CODE
        if not self.readonly:
            print('Not readonly')
            attrs = self.attribute.split('__')
            print('Attrs:', attrs)
            print(attrs[-1])
            for attr in attrs[:-1]:
                obj = getattr(obj, attr, None)
                print('Obj:', obj)
            cleaned = self.clean(data, **kwargs)
            print('Cleaned', cleaned)
            if cleaned is not None or self.saves_null_values:
                if not is_m2m:
                    obj.set_current_language(language)
                    setattr(obj, attrs[-1], cleaned)
                    print(obj._current_language)
                else:
                    getattr(obj, attrs[-1]).set(cleaned)
