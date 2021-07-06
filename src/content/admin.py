from django.contrib import admin
from .models import Question, AnswerOption, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset
from parler import admin as parler_admin


class AnswerOptionInline(parler_admin.TranslatableStackedInline):
    model = AnswerOption
    extra = 0


class QuestionImageAssetInline(admin.TabularInline):
    model = QuestionImageAsset
    extra = 0


class QuestionVideoAssetInline(admin.TabularInline):
    model = QuestionVideoAsset
    extra = 0


class QuestionAudioAssetInline(admin.TabularInline):
    model = QuestionAudioAsset
    extra = 0


@admin.register(AnswerOption)
class AnswerOptionAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(parler_admin.TranslatableAdmin):
    inlines = [AnswerOptionInline,
               QuestionImageAssetInline,
               QuestionVideoAssetInline,
               QuestionAudioAssetInline]
