from django.shortcuts import render
from .models import Person

def chore_assignments_view(request):
    people = Person.objects.select_related('chore_group').prefetch_related('chore_group__chores')
    return render(request, "chores/assignments.html", {"people": people})