from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class BlockConfigurationKeyword(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
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

class BlockType(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
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

class BlockTypeConfiguration(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for key-value pairs for a block tpye
    Examples:
        - Show Timer: True
    """
	PREFIX = 'blck_typ_cnfg_'
	block_type = models.ForeignKey('block.BlockType', on_delete=models.PROTECT, null=True)
	key = models.ForeignKey('block.BlockConfigurationKeyword', on_delete=models.PROTECT, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)

class Block(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_'

	MODALITY_AI = 'AI'
	MODALITY_PATH = 'PATH'
    MODALITY_PRACTICE = 'PRACTICE'
    MODALITY_CHOICES = (
        (MODALITY_AI, 'AI'),
        (MODALITY_PATH, 'Choose your path'),
        (MODALITY_PRACTICE, 'Practice'),
    )

	modality = models.ChoiceField(choices=MODALITY_CHOICES, default=MODALITY_AI)
    first_presentation_timestamp = models.DateTimeField(null=True)
    last_presentation_timestamp = models.DateTimeField(null=True)

    type_of = models.ForeignKey('block.BlockType', on_delete=models.PROTECT, null=True)
	student =  models.ManyToManyField('students.Student', null=True, blank=True)
    topics =  models.ManyToManyField('kb.topics.Topic', null=True, blank=True)
	questions = models.ManyToManyField('content.questions.Question', through='block.BlockQuestion')
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
            if self.type_of:
                for item in self.type_of.blocktypeconfiguration_set.all():
                    self.blockconfiguration_set.create(
                        key=item.key,
                        value=item.value,
                        data_type=item.data_type
                    )


        return sve


class BlockConfiguration(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for key-value pairs for a block tpye
    Examples:
        - Show Timer: True
    """
	PREFIX = 'blck_cnfg_'
	
	block = models.ForeignKey('block.Block', on_delete=models.PROTECT, null=True)
	key = models.ForeignKey('block.BlockConfigurationKeyword', on_delete=models.PROTECT, null=True)
	data_type  = models.CharField(max_length=128, null=True)
	value  = models.CharField(max_length=128, null=True)
	

class BlockPresentation(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
	PREFIX = 'blck_pres_'

    # TODO: borrar. block_configuration = models.ForeignKey(BlockConfiguration, on_delete=models.PROTECT, null=True)
	hits = models.IntegerField(max_length=20, null=True)
	errors = models.IntegerField(max_length=20, null=True)
	total = models.IntegerField(max_length=20, null=True)
	points = models.IntegerField(max_length=20, null=True)
	start_timestamp = models.DateTimeField(null=True)
	end_timestamp = models.DateTimeField(null=True)	



class BlockQuestion(TimestampModel, RandomSlugModel):
    """
    This model will contain ALL the questions of the block, independently of the presentation of them on block presentation.
    """
    STATUS_PENDING = 'Pending'
    STATUS_CORRECT = 'Correct'
    STATUS_INCORRECT = 'Incorrect'
    STATUS_CHOICES = (
        (STATUS_PENDING,'Pending'),
        (STATUS_CORRECT,'Correct'),
        (STATUS_INCORRECT,'Incorrect'),
    )
    # TODO: estos elementos de choices van al reves 

    block = models.ForeignKey(Block, on_delete=models.PROTECT, null=True)
    question = models.ForeignKey('content.questions.Question', on_delete=models.PROTECT, null=True)
    chosen_answer = models.ForeignKey('content.questions.AnswerOption', on_delete=models.PROTECT, null=True)
    
    is_correct = models.BooleanField(null=True)
    is_answered = models.BooleanField(null=True, default=False)
    status = models.ChoiceField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    def save
        #save here the status according to business logic


class BlockQuestionPresentation(TimestampModel, RandomSlugModel):
    """
    This model will have every presentation of question
    """
    question = models.ForeignKey('content.questions.Question', on_delete=models.PROTECT, null=True)
    block_question = models.ForeignKey('block.BlockQuestion', on_delete=models.PROTECT, null=True)
	presentation_timestamp = models.DateTimeField(null=True)
	submission_timestamp = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.question = self.block_question.question
        sve = super().save(*args, **kwargs)
        return sve


