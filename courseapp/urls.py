from django.urls import path
from . import views

urlpatterns = [
    path('lesson/<int:lesson_id>/submit/', views.submit, name='submit'),
    path('submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
