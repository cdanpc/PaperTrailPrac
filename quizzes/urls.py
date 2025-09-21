from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list_view, name='quiz_list'),
    path('<int:pk>/', views.quiz_detail_view, name='quiz_detail'),
    path('<int:pk>/take/', views.take_quiz_view, name='take_quiz'),
    path('create/', views.create_quiz_view, name='create_quiz'),
    path('<int:pk>/add-questions/', views.add_questions_view, name='add_questions'),
    path('my-quizzes/', views.my_quizzes_view, name='my_quizzes'),
]
