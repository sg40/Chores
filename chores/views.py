from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Person, Chore
from .forms import ChoreCompletionForm

def chore_assignments_view(request):
    people = Person.objects.select_related('chore_group').prefetch_related('chore_group__chores__days')

    if request.method == 'POST':
        chore_id = request.POST.get('chore_id')
        if chore_id:
            chore = get_object_or_404(Chore, id=chore_id)
            form = ChoreCompletionForm(request.POST, instance=chore)
            if form.is_valid():
                form.save()
                messages.success(request, f"Chore '{chore.name}' marked as {'complete' if chore.completed else 'incomplete'}.")
            else:
                messages.error(request, "Invalid form submission.")
        else:
            messages.error(request, "Invalid chore ID.")
        return redirect('chore_assignments')

    return render(request, 'chores/assignments.html', {'people': people})

def chore_detail_view(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    return render(request, "chores/chore_detail.html", {"chore": chore})
