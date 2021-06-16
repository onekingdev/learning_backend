from django.contrib import admin
from .models import Question, AnswerOption, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset
from parler import admin as parler_admin



# Register your models here.
class AnswerOptionInline(parler_admin.TranslatableStackedInline):
    model = AnswerOption

class QuestionImageAssetInline(admin.TabularInline):
    model = QuestionImageAsset

class QuestionVideoAssetInline(admin.TabularInline):
    model = QuestionVideoAsset

class QuestionAudioAssetInline(admin.TabularInline):
    model = QuestionAudioAsset

@admin.register(AnswerOption)
class AnswerOptionAdmin(parler_admin.TranslatableAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(parler_admin.TranslatableAdmin):
    inlines = [ QuestionImageAssetInline, QuestionVideoAssetInline, QuestionAudioAssetInline, AnswerOptionInline]

