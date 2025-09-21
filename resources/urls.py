from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resource_list_view, name='resource_list'),
    path('<int:pk>/', views.resource_detail_view, name='resource_detail'),
    path('upload/', views.upload_resource_view, name='upload_resource'),
    path('<int:pk>/review/', views.add_review_view, name='add_review'),
    path('<int:pk>/bookmark/', views.bookmark_resource_view, name='bookmark_resource'),
    path('bookmarks/', views.my_bookmarks_view, name='my_bookmarks'),
]
