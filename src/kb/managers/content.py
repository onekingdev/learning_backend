from app.models import ActiveManager
from parler.models import TranslatableManager
from parler.managers import TranslatableQuerySet
from polymorphic.models import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class QuestionManager(ActiveManager, TranslatableManager):
    pass


class AnswerOptionQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class AnswerOptionManager(TranslatableManager, PolymorphicManager):
    queryset_class = AnswerOptionQuerySet
