from django.db import models
from django.utils.text import slugify
from people.students.models import Student
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class BlockConfigurationKeyword(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for cofig keyword.
    Examples:
        - show timer
        - allow to pass on questions
    """
	PREFIX = 'blck_cnfg_key_'
	name  = models.CharField(max_length=128, null=True)

	def __str__(self):
        return self.name

class BlockType(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for types of blocks. These take some config values and are copy pasted to blocks upon block generation
    Examples:
        - Assessment
        - Beat The Clock
    """
	PREFIX = 'blck_typ_'
	name  = models.CharField(max_length=128, null=True)
	
	def __str__(self):
        return self.name

class BlockTypeConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for key-value pairs for a block tpye
    Examples:
        - Show Timer: True
    """
	PREFIX = 'blck_typ_cnfg_'
	block_type = models.ForeignKey(BlockType, on_delete=models.CASCADE, null=True)
	key = models.ForeignKey(BlockConfigurationKeyword, on_delete=models.CASCADE, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)

class Block(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_'

	type_of = models.ForeignKey(BlockType, on_delete=models.PROTECT, null=True)
	# modality = es un modelo o un choice. tipicamente AI, Pick your path, Practice
	student =  models.ManyToManyField(Student, on_delete=models.PROTECT, null=True, blank=True)
	first_presentation_timestamp = models.DateTimeField(null=True)
	last_presentation_timestamp = models.DateTimeField(null=True)
    # topics m2m kb topic
    # questions = models.ManyToManyField('content.questions.Question', through=BlockQuestion), quizas mejor por question_set
    # engangement points
    # coins earned

    def save(self, *args, **kwargs):
        is_new = False
        if not self.pk:
            is_new = True

        sve = super().save(*args, **kwargs)

        if is_new:
            # TODO: aqui falta hacer el copy paste de las configs, si es nuevo
            # TODO: por cada key-value del type of, hay que nutrir el hijo de esta tabla 

        return sve


class BlockConfiguration(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for key-value pairs for a block tpye
    Examples:
        - Show Timer: True
    """
	PREFIX = 'blck_cnfg_'
	
	block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
	key = models.ForeignKey(BlockConfigurationKeyword, on_delete=models.CASCADE, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)
	

class BlockPresentation(TimestampModel, UUIDModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_pres_'

    # TODO: borrar. block_configuration = models.ForeignKey(BlockConfiguration, on_delete=models.CASCADE, null=True)
	hits = models.IntegerField(max_length=20, null=True)
	errors = models.IntegerField(max_length=20, null=True)
	total = models.IntegerField(max_length=20, null=True)
	points = models.IntegerField(max_length=20, null=True)
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)	



class BlockQuestion():
    """
    This model will contain ALL the questions of the block, independently of the presentation of them on block presentation.
    """
    STATUS_PENDING = 'Pending'
    STATUS_CORRECT = 'Correct'
    STATUS_INCORRECT = 'Incorrect'
    STATUS_CHOICES = (
        ('Pending',STATUS_PENDING),
        ('Correct',STATUS_CORRECT),
        ('Incorrect',STATUS_INCORRECT),
    )
    # block = FK a block
    question fk a question
    chosen_answer FK a options
    is_correct Bool Nuul
    is_answered Bool Default False

    status = models.ChoiceField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    def save
        #save here the status according to business logic


class BlockQuestionPresentation():
    """
    This model will have every presentation of question
    """
    question # this is for efficiency on db, por facilidad de acceso, editable false, null=true
    block_question fk a BlockQuestion
	presentation_timestamp = models.DateTimeField(null=True)
	submission_timestamp = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.question = self.block_question.question
        sve = super().save(*args, **kwargs)
        return sve


