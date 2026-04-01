from django.urls import path
from .views import *
from .views import login_view, dashboard, start_exam, exam_view, submit_exam, result_view

urlpatterns = [
    path('', login_view, name='login'),   # default page
    path('dashboard/', dashboard, name='dashboard'),
    path('start/', start_exam, name='start_exam'),
    path('exam/', exam_view, name='exam'),
    path('submit/', submit_exam, name='submit'),
    path('signup/', signup_view, name='signup'),
    path('results/', result_view, name='results'),
]