import random
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import(
    BlockType,
    BlockAssignment,
    Block,
    BlockQuestionPresentation,
    StudentBlockQuestionPresentationHistory,
    BlockConfiguration,
    BlockConfigurationKeyword,
    BlockTypeConfiguration,
    BlockPresentation,
    BlockTransaction
)
from kb.models.content import Question
from parler import admin as parler_admin


# Register your models here.
@admin.register(BlockType)
class BlockTypeAdmin(parler_admin.TranslatableAdmin):
    list_display = ('id', 'name', 'is_active',)
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(BlockAssignment)
class BlockAssignmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'order_number', 'student', 'block_identifier', 'block_topic_grade', 'block_modality', 'order')
    search_fields = ('order_number', 'student', 'block_identifier')
    list_filter = ('block__modality',)

    @admin.display(description='Block identifier')
    def block_identifier(self, obj):
        return ("%s" % (obj.block.random_slug))

    @admin.display(description='Block topic grade')
    def block_topic_grade(self, obj):
        return ("%s" % (obj.block.topic_grade))

    @admin.display(description='Block modality')
    def block_modality(self, obj):
        return ("%s" % (obj.block.modality))

    @admin.display(description='Order')
    def order_number(self, obj):
        return ("%s" % (obj.order))


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_grade', 'modality', 'random_slug',)
    search_fields = ('topic_grade', 'modality')
    list_filter = ('modality', 'random_slug',)
    autocomplete_fields = ['questions', 'topic_grade']

    def save_related(self, request, form, formsets, change):
        super(BlockAdmin, self).save_related(request, form, formsets, change)

        if form.instance.questions.name is None:
            available_questions = list(
                Question.objects.filter(
                    topic=form.instance.topic_grade.topic).filter(
                    grade=form.instance.topic_grade.grade))
            if len(available_questions) < form.instance.block_size:
                for question in available_questions:
                    form.instance.questions.add(question)
            else:
                random_questions = random.sample(
                    available_questions, form.instance.block_size)
                for question in random_questions:
                    form.instance.questions.add(question)

        for student in form.instance.students.all():
            BlockAssignment.objects.get_or_create(
                block=form.instance, student=student)


@admin.register(BlockQuestionPresentation)
class BlockQuestionPresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_timestamp', 'block_presentation', 'question', 'typed_answer', 'topic', 'status')
    search_fields = ('block_presentation', 'question', 'typed_answer', 'topic',)
    list_filter = ('create_timestamp', 'status',)
    autocomplete_fields = ['question', 'topic', 'chosen_answer']


@admin.register(BlockConfiguration)
class BlockConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'block', 'key', 'value')
    search_fields = ('block', 'key', 'value',)


@admin.register(BlockConfigurationKeyword)
class BlockConfigurationKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(BlockTypeConfiguration)
class BlockTypeConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'block_type', 'key', 'value', 'is_active')
    search_fields = ('block_type', 'key', 'value',)
    list_filter = ('is_active',)


@admin.register(BlockPresentation)
class BlockPresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'block', 'student', 'hits', 'errors', 'total', 'points', 'bonusCoins',
                    'coins', 'start_timestamp', 'end_timestamp', 'is_active')
    search_fields = ('block', 'student',)
    list_filter = ('start_timestamp', 'end_timestamp', 'is_active',)


@admin.register(StudentBlockQuestionPresentationHistory)
class StudentBlockQuestionPresentationHistory(admin.ModelAdmin):
    list_display = ('id', 'student')
    search_fields = ('student',)


@admin.register(BlockTransaction)
class BlockTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'blockPresentation')
    search_fields = ('blockPresentation',)
