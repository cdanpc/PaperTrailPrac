from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcard_list_view, name='flashcard_list'),
    path('<int:pk>/', views.flashcard_detail_view, name='flashcard_detail'),
    path('<int:pk>/study/', views.study_flashcard_view, name='study_flashcard'),
    path('create/', views.create_flashcard_view, name='create_flashcard'),
    path('<int:pk>/add-items/', views.add_items_view, name='add_items'),
    path('my-flashcards/', views.my_flashcards_view, name='my_flashcards'),
]
