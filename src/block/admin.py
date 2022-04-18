import random
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import BlockType, BlockAssignment, Block, BlockQuestionPresentation
from kb.models.content import Question
from parler import admin as parler_admin


# Register your models here.
@admin.register(BlockType)
class BlockTypeAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(BlockAssignment)
class BlockAssignmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        'order_number',
        'student',
        'block_identifier',
        'block_topic_grade',
        'block_modality',
        'order'
    )

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
    list_display = (
        'topic_grade',
        'id',
        'modality',
        'random_slug',
    )
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
    list_display = (
        'id',
        'created_timestamp',
        'block_presentation',
        'question',
        'typed_answer',
        'topic',
        'status',
    )

    autocomplete_fields = ['question']
