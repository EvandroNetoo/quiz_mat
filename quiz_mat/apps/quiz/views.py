from asgiref.sync import sync_to_async
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404, render
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from quiz.forms import AnswerExerciseForm, ExerciseForm
from quiz.models import Exercise


class HomeView(View):
    template_name = 'quiz/home.html'

    async def get(self, request: HttpRequest):
        exercises = await sync_to_async(list)(
            Exercise.objects.all().select_related('created_by')
        )
        context = {
            'exercises': exercises,
        }
        return render(request, self.template_name, context)


class AddExerciseView(View):
    template_name = 'quiz/add_exercise.html'
    form_class = ExerciseForm

    async def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    async def post(self, request: ASGIRequest):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        exercise = form.save(commit=False)
        exercise.created_by = request.user
        await exercise.asave()
        return HttpResponseClientRedirect(reverse('home'))


class AnswerExerciseView(View):
    template_name = 'quiz/answer_exercise.html'
    form_class = AnswerExerciseForm

    async def get(self, request: HttpRequest, exercise_id: str):
        exercise = await aget_object_or_404(Exercise, id=exercise_id)
        context = {
            'exercise': exercise,
            'question': exercise.generate(),
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    async def post(self, request: HttpRequest, exercise_id: str):
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        correct_answer = float(request.POST.get('correct_answer'))
        answer = form.cleaned_data.get('answer')
        if correct_answer != answer:
            form.add_error(None, 'Resposta incorreta! tente novamente.')
        else:
            form.add_error(None, 'Resposta Correta! Boa!')
        context = {
            'form': form,
        }
        return render(request, 'components/form.html', context)
