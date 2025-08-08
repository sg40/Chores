
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.chore_assignments_view, name='chore_assignments'),
    path('add-chore/', views.ChoreCreateView.as_view(), name='add_chore'),
    path('chore/<int:pk>/', views.chore_detail_view, name='chore_detail'),
    path('modify-chores/', views.modify_chores, name='modify_chores'),
    path('modify-chores/<int:chore_id>/', views.edit_chore, name='edit_chore'),
]
