from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, Chore
from .forms import ChoreCompletionForm

def chore_assignments_view(request):
    people = Person.objects.select_related('chore_group').prefetch_related('chore_group__chores__days')

    if request.method == 'POST':
        form = ChoreCompletionForm(request.POST)
        if form.is_valid():
            chore = form.save()
            return redirect('chore_assignments')  # Redirect after form submission to avoid resubmitting on refresh
    else:
        form = ChoreCompletionForm()

    return render(request, 'chores/assignments.html', {'people': people, 'form': form})

def chore_detail_view(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    return render(request, "chores/chore_detail.html", {"chore": chore})

