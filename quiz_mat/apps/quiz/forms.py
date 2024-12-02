from django import forms

from quiz.models import Exercise


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            'title',
            'question',
            'formula',
        ]


class AnswerExerciseForm(forms.Form):
    answer = forms.FloatField(label='Reposta')
