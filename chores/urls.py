from django.urls import path
from .views import chore_assignments_view

urlpatterns = [
    path('', chore_assignments_view, name='chore_assignments'),
]
