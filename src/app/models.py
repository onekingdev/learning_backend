import uuid
from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def inactive_objects(self):
        return super().get_queryset().filter(is_active=False)



class BaseModel(models.Model):

    PREFIX = ''
    identifier = models.CharField(editable=False, unique=True, max_length=128)

    def get_identifier(self):
        return'{prefix}{id:04}'.format(prefix=self.PREFIX, id=self.pk)

    def save(self, *args, **kwargs):
        self.identifier = self.get_identifier()
        sup = super().save(*args, **kwargs)
        return sup

    def __str__(self):
        valid_str_names = ('name',)
        for valid_str in valid_str_names:
            if hasattr(self, valid_str):
                return getattr(self, valid_str)
        return super().__str__()

    def get_meta(self):
        return self._meta

    class Meta:
        abstract = True


class RandomSlugModel(BaseModel):

    SLUG_LENGTH = 10
    random_slug = models.SlugField(editable=False, unique=True)

    def get_identifier(self):
        return '{prefix}{slug}'.format(prefix=self.PREFIX, slug=self.random_slug)

    def save(self, *args, **kwargs):
        if not self.random_slug:
            while True:
                random_slug = uuid.uuid4().hex[:self.SLUG_LENGTH].upper()
                others = self._meta.model.objects.filter(random_slug=random_slug)
                if others.count() == 0:
                    self.random_slug = random_slug
                    break
        sup = super().save(*args, **kwargs)
        return sup

    class Meta:
        abstract = True


class UUIDModel(BaseModel):

    random_slug = models.UUIDField(editable=False, unique=True)

    def get_identifier(self):
        return '{prefix}{slug}'.format(prefix=self.PREFIX, slug=self.random_slug)

    def save(self, *args, **kwargs):
        if not self.random_slug:
            while True:
                random_slug = uuid.uuid4()
                others = self._meta.model.objects.filter(random_slug=random_slug)
                if others.count() == 0:
                    self.random_slug = random_slug
                    break
        sup = super().save(*args, **kwargs)
        return sup

    class Meta:
        abstract = True


class TimestampModel(models.Model):

    create_timestamp = models.DateTimeField('Timestamp de creación', auto_now_add=True, editable=False)
    update_timestamp = models.DateTimeField('Timestamp de modificación', auto_now=True, editable=False)

    class Meta:
        abstract = True

