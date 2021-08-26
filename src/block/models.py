from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager


class BlockTypeManager(ActiveManager, TranslatableManager):
    pass


class BlockType(
        TimestampModel,
        RandomSlugModel,
        IsActiveModel,
        TranslatableModel):
    """
    Model for types of blocks. These take some config values and are copy pasted to blocks upon block generation
    Examples:
    - Assessment
    - Beat The Clock
    """

    PREFIX = 'block_type_'

    # Attributes
    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True)
    )
    objects = BlockTypeManager()


class BlockTypeConfiguration(TimestampModel, IsActiveModel):
    """
    Model for key-value pairs for a block type
    Examples:
    - Show Timer: True
    """

    # FK's
    block_type = models.ForeignKey(
        'block.BlockType',
        on_delete=models.PROTECT,
        null=True
    )
    key = models.ForeignKey(
        'block.BlockConfigurationKeyword',
        on_delete=models.PROTECT,
        null=True
    )

    # Attributes
    value = models.CharField(max_length=128, null=True)


class Block(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'block_'

    MODALITY_AI = 'AI'
    MODALITY_PATH = 'PATH'
    MODALITY_PRACTICE = 'PRACTICE'
    MODALITY_CHOICES = (
        (MODALITY_AI, 'AI'),
        (MODALITY_PATH, 'Choose your path'),
        (MODALITY_PRACTICE, 'Practice'),
    )

    # FK's
    type_of = models.ForeignKey(
        'block.BlockType',
        on_delete=models.PROTECT,
        null=True
    )
    # Why the need for students in the block?
    student = models.ManyToManyField('students.Student', blank=True)
    topics = models.ManyToManyField(
        'kb.Topic',
        blank=True,
        help_text='These are the topics covered in this block'
    )

    # Attributes
    modality = models.CharField(
        max_length=128,
        choices=MODALITY_CHOICES,
        default=MODALITY_AI
    )
    first_presentation_timestamp = models.DateTimeField(null=True)
    last_presentation_timestamp = models.DateTimeField(null=True)
    questions = models.ManyToManyField(
        'content.Question',
        through='block.BlockQuestion'
    )

    # Metrics
    engangement_points_available = models.PositiveSmallIntegerField(null=True)
    coins_available = models.PositiveSmallIntegerField(null=True)
    battery_points_available = models.PositiveSmallIntegerField(default=1, null=True)
    # engangement_points_earned = models.PositiveSmallIntegerField(null=True)
    # coins_earned = models.PositiveSmallIntegerField(null=True)
    # battery_points_earned = models.PositiveSmallIntegerField(null=True)

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
                    )
        return sve


class BlockConfiguration(TimestampModel):
    """
    Model for key-value pairs for a block
    Examples:
    - Show Timer: True
    """

    # FK's
    block = models.ForeignKey(
        'block.Block',
        on_delete=models.PROTECT,
        null=True
    )
    key = models.ForeignKey(
        'block.BlockConfigurationKeyword',
        on_delete=models.PROTECT,
        null=True
    )

    # Attributes
    value = models.CharField(max_length=128, null=True)


class BlockConfigurationKeyword(TimestampModel, IsActiveModel):
    """
    Model for config keyword.
    Examples:
    - show timer
    - allow to pass on questions
    """

    # Attributes
    name = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name


class BlockPresentation(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'block_presentation_'

    # FK's
    block = models.ForeignKey(
        'block.Block',
        on_delete=models.CASCADE,
        null=True
    )

    # Metrics
    hits = models.IntegerField(null=True)
    errors = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(null=True)


class BlockQuestion(TimestampModel, RandomSlugModel):
    """
    This model contains ALL the questions of the block, independently of the presentation of them on BlockPresentation.
    Used for M2M relation between block and question.
    """

    STATUS_PENDING = 'PENDING'
    STATUS_CORRECT = 'CORRECT'
    STATUS_INCORRECT = 'INCORRECT'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CORRECT, 'Correct'),
        (STATUS_INCORRECT, 'Incorrect'),
    )

    # FK's
    block = models.ForeignKey(Block, on_delete=models.PROTECT, null=True)
    question = models.ForeignKey(
        'content.Question',
        on_delete=models.PROTECT,
        null=True
    )
    chosen_answer = models.ForeignKey(
        'content.AnswerOption',
        on_delete=models.SET_NULL,
        null=True
    )

    # Metrics
    is_correct = models.BooleanField(null=True)
    is_answered = models.BooleanField(null=True, default=False)
    status = models.CharField(
        max_length=128,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    def save(self, *args, **kwargs):
        if self.chosen_answer:
            self.is_answered = True
            if self.chosen_answer.is_correct:
                self.is_correct = True
                self.status = self.STATUS_CORRECT
            else:
                self.is_correct = False
                self.status = self.STATUS_INCORRECT
        else:
            self.is_answered = False
            self.status = self.STATUS_PENDING

        return super().save(*args, **kwargs)


class BlockQuestionPresentation(TimestampModel, RandomSlugModel):
    """
    This model is used for registering when questions are presented and submitted
    """

    # FK's
    question = models.ForeignKey(
        'content.Question',
        on_delete=models.PROTECT,
        null=True
    )
    block_question = models.ForeignKey(
        'block.BlockQuestion',
        on_delete=models.PROTECT,
        null=True
    )
    presentation_timestamp = models.DateTimeField(null=True)
    submission_timestamp = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.question = self.block_question.question
        return super().save(*args, **kwargs)
