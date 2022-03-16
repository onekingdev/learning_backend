from app.models import ActiveManager
from parler.models import TranslatableManager


class QuestionManager(ActiveManager, TranslatableManager):
    pass
