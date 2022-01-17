from app.resources import TranslatableModelResource
from app.widgets import TranslatableForeignKeyWidget
from import_export.fields import Field
from import_export.resources import ModelResource
from .models import Audience


class AudienceResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    class Meta:
        model = Audience
        skip_unchanged = True
        report_skipped = False
