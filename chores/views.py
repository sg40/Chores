from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User, Chore, ChoreGroup, Days
from .forms import ChoreCompletionForm, ChoreForm, LoginForm

def chore_assignments_view(request):
    people = User.objects.select_related('chore_group').prefetch_related('chore_group__chores__days')
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
    from chores.models import RotationLog
    last_rotation = RotationLog.objects.order_by('-rotation_time').first()
    return render(request, 'chores/assignments.html', {
        'people': people,
        'last_rotation_time': last_rotation.rotation_time if last_rotation else None
    })

def chore_detail_view(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    return render(request, "chores/chore_detail.html", {"chore": chore})

class ChoreCreateView(CreateView):
    model = Chore
    form_class = ChoreForm
    template_name = 'chores/add_chore.html'
    success_url = reverse_lazy('modify_chores')

    def get_initial(self):
        initial = super().get_initial()
        group_id = self.request.GET.get('group_id')
        if group_id:
            try:
                group = ChoreGroup.objects.get(id=group_id)
                initial['chore_group'] = group
            except ChoreGroup.DoesNotExist:
                messages.error(self.request, "Invalid chore group selected.")
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_id'] = self.request.GET.get('group_id')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Chore '{form.cleaned_data['name']}' added successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

def modify_chores(request):
    chore_groups = ChoreGroup.objects.all()
    if request.method == 'POST':
        chore_id = request.POST.get('chore_id')
        chore = get_object_or_404(Chore, id=chore_id)
        chore.delete()
        messages.success(request, f'Chore "{chore.name}" deleted successfully.')
        return redirect('modify_chores')
    return render(request, 'chores/modify_chores.html', {'chore_groups': chore_groups})

def edit_chore(request, chore_id):
    chore = get_object_or_404(Chore, id=chore_id)
    chore_groups = ChoreGroup.objects.all()
    all_days = Days.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        group_id = request.POST.get('chore_group')
        day_ids = request.POST.getlist('days')
        if not name:
            messages.error(request, 'Chore name is required.')
            return render(request, 'chores/edit_chore.html', {'chore': chore, 'chore_groups': chore_groups, 'all_days': all_days})
        if not group_id:
            messages.error(request, 'Please select a chore group.')
            return render(request, 'chores/edit_chore.html', {'chore': chore, 'chore_groups': chore_groups, 'all_days': all_days})
        try:
            group = ChoreGroup.objects.get(id=group_id)
            chore.name = name
            chore.description = description
            chore.chore_group = group
            chore.save()
            if day_ids:
                chore.days.set(day_ids)
            else:
                chore.days.clear()
            messages.success(request, f'Chore "{name}" updated successfully.')
            return redirect('modify_chores')
        except ChoreGroup.DoesNotExist:
            messages.error(request, 'Invalid chore group selected.')
            return render(request, 'chores/edit_chore.html', {'chore': chore, 'chore_groups': chore_groups, 'all_days': all_days})
        except Days.DoesNotExist:
            messages.error(request, 'Invalid day selected.')
            return render(request, 'chores/edit_chore.html', {'chore': chore, 'chore_groups': chore_groups, 'all_days': all_days})
    return render(request, 'chores/edit_chore.html', {'chore': chore, 'chore_groups': chore_groups, 'all_days': all_days})

def login_view(request):
    if request.session.get('user_id'):
        return redirect('chore_assignments')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['is_admin'] = user.admin
            return redirect('chore_assignments')
    else:
        form = LoginForm()
    
    return render(request, 'chores/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')