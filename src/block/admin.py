import random
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import BlockType, BlockAssignment, Block
from kb.models.content import Question
from parler import admin as parler_admin


# Register your models here.
@admin.register(BlockType)
class BlockTypeAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(BlockAssignment)
class BlockAssignmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        print("Saving related")
        super(BlockAdmin, self).save_related(request, form, formsets, change)

        if form.instance.questions.name is None:
            print("Questions are NOne")
            available_questions = list(
                Question.objects.filter(topic_grade=form.instance.topic_grade))
            if len(available_questions) < form.instance.block_size:
                for question in available_questions:
                    form.instance.questions.add(question)
            else:
                random_questions = random.sample(
                    available_questions, self.block_size)
                for question in random_questions:
                    form.instance.questions.add(question)
