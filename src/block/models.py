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
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, null=True)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class BlockType(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for types of blocks. These take some config values and are copy pasted to blocks upon block generation
    Examples:
        - Assessment
        - Beat The Clock
    """
    PREFIX = 'blck_typ_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, null=True)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class BlockTypeConfiguration(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    """
    Model for key-value pairs for a block tpye
    Examples:
        - Show Timer: True
    """
    PREFIX = 'blck_typ_cnfg_'
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
    modality = models.CharField(max_length=128, choices=MODALITY_CHOICES, default=MODALITY_AI)
    first_presentation_timestamp = models.DateTimeField(null=True)
    last_presentation_timestamp = models.DateTimeField(null=True)

    type_of = models.ForeignKey('block.BlockType', on_delete=models.PROTECT, null=True)
    student =  models.ManyToManyField('students.Student', blank=True)
    topics =  models.ManyToManyField('kb.Topic', blank=True)
    questions = models.ManyToManyField('content.Question', through='block.BlockQuestion')
    engangement_points = models.IntegerField(null=True)
    coins_earned = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        is_new = False
        if not self.pk:
            is_new = True

        sve = super().save(*args, **kwargs)

        if is_new:
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
    id = models.AutoField(primary_key=True)
    block = models.ForeignKey('block.Block', on_delete=models.PROTECT, null=True)
    key = models.ForeignKey('block.BlockConfigurationKeyword', on_delete=models.PROTECT, null=True)
    data_type  = models.CharField(max_length=128, null=True)
    value  = models.CharField(max_length=128, null=True)
    

class BlockPresentation(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'blck_pres_'

    # TODO: borrar. block_configuration = models.ForeignKey(BlockConfiguration, on_delete=models.PROTECT, null=True)
    id = models.AutoField(primary_key=True)
    hits = models.IntegerField(null=True)
    errors = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(null=True) 

    class Meta:
        ordering = ['create_timestamp']

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
    id = models.AutoField(primary_key=True)
    block = models.ForeignKey(Block, on_delete=models.PROTECT, null=True)
    question = models.ForeignKey('content.Question', on_delete=models.PROTECT, null=True)
    chosen_answer = models.ForeignKey('content.AnswerOption', on_delete=models.PROTECT, null=True)
    
    is_correct = models.BooleanField(null=True)
    is_answered = models.BooleanField(null=True, default=False)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default=STATUS_PENDING)

    #def save
        #save here the status according to business logic


class BlockQuestionPresentation(TimestampModel, RandomSlugModel):
    """
    This model will have every presentation of question
    """
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey('content.Question', on_delete=models.PROTECT, null=True)
    block_question = models.ForeignKey('block.BlockQuestion', on_delete=models.PROTECT, null=True)
    presentation_timestamp = models.DateTimeField(null=True)
    submission_timestamp = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.question = self.block_question.question
        sve = super().save(*args, **kwargs)
        return sve


