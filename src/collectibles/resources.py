from app.resources import TranslatableModelResource
from app.widgets import TranslatableForeignKeyWidget
from import_export.fields import Field
from import_export.resources import ModelResource
from .models import Collectible


class CollectibleResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )


    description = Field(
        attribute='description'
    )

    class Meta:
        model = Collectible
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'language_code',
            'name',
            'description',
            'category',
            'image',
            'tier',
        )
