from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class BlockConfigurationKeyword(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_cnfg_key_'
	"""
		name CharField
	"""

class BlockType(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_typ_'
	"""
		name CharField
	"""
	"""
		type_of => Examples
			Beat the clock
			Refresher
			Question & Answer
			Assessment
	"""
class BlockTypeConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_typ_cnfg_'
	"""
		block_type ForeignKey(BlockType)
		key ForeignKey(BlockConfigurationKeyword)
		data_type CharField
		value CharField
	"""

class Block(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_'

	"""
		modality CharField(choices)
		student ManyToMany
		first_presentation_timestamp DateTimeField
		last_presentation_timestamp DateTimeField
	"""

class BlockConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_cnfg_'
	"""
		block ForeignKey(Block)
		key ForeignKey(BlockConfigurationKeyword)
		data_type CharField
		value CharField
	"""

class BlockPresentation(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_pres_'
	"""
		hits IntegerField
		errors IntegerField
		total IntegerField
		points IntegerField
		start_timestamp DateTimeField
		end_timestamp DateTimeField
	"""

	