from django.urls import path
from .views import chore_assignments_view, chore_detail_view

urlpatterns = [
    path('', chore_assignments_view, name='chore_assignments'),
    path('chore/<int:pk>/', chore_detail_view, name='chore_detail'),
]
