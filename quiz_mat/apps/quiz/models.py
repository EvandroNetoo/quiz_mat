import random

from accounts.models import User
from django.db import models
from utils.models import TimeStampedModel


class Exercise(TimeStampedModel):
    created_by = models.ForeignKey(
        User, models.SET_NULL, null=True, verbose_name='criado por'
    )
    title = models.CharField('título', max_length=50)
    question = models.TextField('questão')
    formula = models.CharField('formúla', max_length=100)

    def __str__(self):
        return self.title

    def generate(self):
        variables = {
            var.strip('{}')
            for var in self.question.split()
            if var.startswith('{') and var.endswith('}')
        }

        values = {var: random.randint(0, 50) for var in variables}  # noqa

        formatted_question = self.question.format(**values)
        formatted_formula = self.formula.format(**values)

        try:
            answer = eval(formatted_formula)  # noqa
        except Exception as e:
            raise ValueError(f'Erro ao avaliar a fórmula: {e}') from None

        return {
            'question': formatted_question,
            'answer': answer,
        }
