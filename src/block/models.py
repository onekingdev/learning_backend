from django.db import models
from django.utils.text import slugify
from people.students.models import Student
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class BlockConfigurationKeyword(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_cnfg_key_'
	name  = models.CharField(max_length=128, null=True)

	def __str__(self):
        return self.name

class BlockType(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_typ_'
	name  = models.CharField(max_length=128, null=True)
	
	def __str__(self):
        return self.name

class BlockTypeConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_typ_cnfg_'
	block_type = models.ForeignKey(BlockType, on_delete=models.CASCADE, null=True)
	key = models.ForeignKey(BlockConfigurationKeyword, on_delete=models.CASCADE, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)

class Block(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_'

	modality = models.ForeignKey(BlockTypeConfiguration, on_delete=models.CASCADE, null=True)
	student =  models.ManyToManyField(Student, on_delete=models.PROTECT, null=True, blank=True)
	first_presentation_timestamp = models.DateTimeField(null=True)
	last_presentation_timestamp = models.DateTimeField(null=True)

class BlockConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_cnfg_'
	
	block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
	key = models.ForeignKey(BlockConfigurationKeyword, on_delete=models.CASCADE, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)
	

class BlockPresentation(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_pres_'

	block_configuration = models.ForeignKey(BlockConfiguration, on_delete=models.CASCADE, null=True)
	hits = models.IntegerField(max_length=20, null=True)
	errors = models.IntegerField(max_length=20, null=True)
	total = models.IntegerField(max_length=20, null=True)
	points = models.IntegerField(max_length=20, null=True)
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)	