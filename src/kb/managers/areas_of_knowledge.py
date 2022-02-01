from app.models import ActiveManager
from parler.managers import TranslatableManager, TranslatableQuerySet


class AreaOfKnowledgeQuerySet(TranslatableQuerySet):

    def as_manager(cls):
        manager = AreaOfKnowledgeManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class AreaOfKnowledgeManager(ActiveManager, TranslatableManager):
    _queryset_class = AreaOfKnowledgeQuerySet
