from django.urls import path
from .views import login_view, dashboard, start_exam, exam_view, submit_exam

urlpatterns = [
    path('', login_view, name='login'),   # default page
    path('dashboard/', dashboard, name='dashboard'),
    path('start/', start_exam, name='start_exam'),
    path('exam/', exam_view, name='exam'),
    path('submit/', submit_exam, name='submit'),
]