import random
from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager
from kb.models.content import Question


class BlockTypeManager(ActiveManager, TranslatableManager):
    pass


class BlockConfiguration(TimestampModel):
    """
    Model for key-value pair configurations for a block.
    These come from the block type configuration and are copied on block creation.
    Examples:
    - Show Timer: True
    """

    # FK's
    block = models.ForeignKey(
        'block.Block',
        on_delete=models.PROTECT,
    )
    key = models.ForeignKey(
        'block.BlockConfigurationKeyword',
        on_delete=models.PROTECT,
    )

    # Attributes
    value = models.CharField(max_length=128, null=True)


class BlockConfigurationKeyword(TimestampModel, IsActiveModel):
    """
    Model for configuration keyword.
    These change the behavior of a block.
    Examples:
    - Show timer
    - Allow to pass on questions
    """

    # Attributes
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class BlockType(
        TimestampModel,
        RandomSlugModel,
        IsActiveModel,
        TranslatableModel):
    """
    Model for types of blocks.
    These take some config values and are copied to blocks upon block creation.
    Examples:
    - Assessment
    - Beat The Clock
    """

    PREFIX = 'block_type_'

    # Attributes
    translations = TranslatedFields(
        name=models.CharField(max_length=128)
    )
    objects = BlockTypeManager()


class BlockTypeConfiguration(TimestampModel, IsActiveModel):
    """
    Model for key-value pairs configurations for a block type
    Examples:
    - Show Timer: True
    """

    # FK's
    block_type = models.ForeignKey(
        'block.BlockType',
        on_delete=models.PROTECT,
    )
    key = models.ForeignKey(
        'block.BlockConfigurationKeyword',
        on_delete=models.PROTECT,
    )

    # Attributes
    value = models.CharField(max_length=128)


class Block(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'block_'

    BLOCK_SIZE = 10

    MODALITY_AI = 'AI'
    MODALITY_PATH = 'PATH'
    MODALITY_PRACTICE = 'HOMEWORK'
    MODALITY_CHOICES = (
        (MODALITY_AI, 'AI'),
        (MODALITY_PATH, 'Choose your path'),
        (MODALITY_PRACTICE, 'Homework'),
    )

    # FK's
    type_of = models.ForeignKey(
        'block.BlockType',
        on_delete=models.PROTECT,
        null=True
    )
    students = models.ManyToManyField(
        'students.Student',
        blank=True
    )
    topic_grade = models.ForeignKey(
        'kb.TopicGrade',
        on_delete=models.PROTECT,
        help_text='This is the topic covered in this block'
    )
    questions = models.ManyToManyField(
        'kb.Question',
    )

    # Attributes
    modality = models.CharField(
        max_length=128,
        choices=MODALITY_CHOICES,
        default=MODALITY_AI
    )
    block_size = models.IntegerField(default=BLOCK_SIZE)

    # Metrics
    engangement_points_available = models.PositiveSmallIntegerField(null=True)
    coins_available = models.PositiveSmallIntegerField(null=True)
    battery_points_available = models.PositiveSmallIntegerField(
        default=1, null=True)

    def save(self, *args, **kwargs):
        is_new = False
        if not self.pk:
            is_new = True

        save = super().save(*args, **kwargs)

        if is_new:
            if self.type_of:
                for item in self.type_of.blocktypeconfiguration_set.all():
                    self.blockconfiguration_set.create(
                        key=item.key,
                        value=item.value,
                    )
            available_questions = list(
                Question.objects.filter(topic_grade=self.topic_grade))
            random_questions = random.sample(
                available_questions, self.block_size)
            for question in random_questions:
                self.questions.add(question)
        return save


class BlockPresentation(TimestampModel, RandomSlugModel):
    PREFIX = 'block_presentation_'

    # FK's
    block = models.ForeignKey(
        Block,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
    )

    # Metrics
    hits = models.IntegerField(null=True)
    errors = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(null=True)


class BlockQuestionPresentation(TimestampModel, RandomSlugModel):
    PREFIX = 'block_question_presentation'

    STATUS_PENDING = 'PENDING'
    STATUS_CORRECT = 'CORRECT'
    STATUS_INCORRECT = 'INCORRECT'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CORRECT, 'Correct'),
        (STATUS_INCORRECT, 'Incorrect'),
    )

    # FK's
    block_presentation = models.ForeignKey(
        BlockPresentation,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        'kb.Question',
        on_delete=models.PROTECT
    )
    chosen_answer = models.ForeignKey(
        'kb.AnswerOption',
        on_delete=models.PROTECT,
        null=True
    )
    topic_grade = models.ForeignKey(
        'kb.TopicGrade',
        on_delete=models.PROTECT,
    )

    # Attributes
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    def is_answered(self):
        if self.status != self.STATUS_PENDING:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.topic_grade = self.block_presentation.block.topic_grade
        if self.chosen_answer:
            if self.chosen_answer.is_correct:
                self.status = self.STATUS_CORRECT
            else:
                self.status = self.STATUS_INCORRECT
        else:
            self.status = self.STATUS_PENDING
