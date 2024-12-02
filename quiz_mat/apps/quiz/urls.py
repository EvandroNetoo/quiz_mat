from apps.quiz import views
from django.urls import path

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home',
    ),
    path(
        'add-exercise/',
        views.AddExerciseView.as_view(),
        name='add_exercise',
    ),
    path(
        'answer/<str:exercise_id>',
        views.AnswerExerciseView.as_view(),
        name='answer_exercise',
    ),
]
