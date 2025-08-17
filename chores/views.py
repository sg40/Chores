from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User, Chore, ChoreGroup, Days
from .forms import ChoreForm, LoginForm

def chore_assignments_view(request):
    people = User.objects.select_related('chore_group').prefetch_related('chore_group__chores__days')
    from chores.models import RotationLog
    from django.utils import timezone
    import calendar
    
    # Get all days ordered by ID for navigation
    all_days = list(Days.objects.all().order_by('id'))
    
    # Get the day to display (from URL parameter or default to today)
    day_id = request.GET.get('day')
    if day_id:
        try:
            current_day = Days.objects.get(id=day_id)
        except Days.DoesNotExist:
            current_day = all_days[0] if all_days else None
    else:
        # Default to today
        weekday = timezone.now().weekday()
        current_day_name = calendar.day_name[weekday]
        
        # Try to find the day in the database with different name formats
        current_day = None
        try:
            # Try exact match first
            current_day = Days.objects.get(name=current_day_name)
        except Days.DoesNotExist:
            try:
                # Try with first 3 letters (e.g., "Mon" instead of "Monday")
                current_day = Days.objects.get(name=current_day_name[:3])
            except Days.DoesNotExist:
                try:
                    # Try with lowercase
                    current_day = Days.objects.get(name=current_day_name.lower())
                except Days.DoesNotExist:
                    # If still not found, get the first day to show something
                    current_day = all_days[0] if all_days else None
    
    # Calculate previous and next days for navigation
    previous_day = None
    next_day = None
    if current_day and all_days:
        try:
            current_index = all_days.index(current_day)
            previous_day = all_days[(current_index - 1) % len(all_days)]
            next_day = all_days[(current_index + 1) % len(all_days)]
        except ValueError:
            previous_day = all_days[0] if all_days else None
            next_day = all_days[0] if all_days else None
    
    last_rotation = RotationLog.objects.order_by('-rotation_time').first()
    return render(request, 'chores/assignments.html', {
        'people': people,
        'current_day': current_day,
        'previous_day': previous_day,
        'next_day': next_day,
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
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user is logged in and is admin
        if not request.session.get('user_id'):
            return redirect('login')
        
        if not request.session.get('is_admin'):
            return redirect('chore_assignments')
        
        return super().dispatch(request, *args, **kwargs)

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
    # Check if user is logged in and is admin
    if not request.session.get('user_id'):
        return redirect('login')
    
    if not request.session.get('is_admin'):
        return redirect('chore_assignments')
    
    chore_groups = ChoreGroup.objects.all()
    if request.method == 'POST':
        chore_id = request.POST.get('chore_id')
        chore = get_object_or_404(Chore, id=chore_id)
        chore.delete()
        messages.success(request, f'Chore "{chore.name}" deleted successfully.')
        return redirect('modify_chores')
    return render(request, 'chores/modify_chores.html', {'chore_groups': chore_groups})

def edit_chore(request, chore_id):
    # Check if user is logged in and is admin
    if not request.session.get('user_id'):
        return redirect('login')
    
    if not request.session.get('is_admin'):
        return redirect('chore_assignments')
    
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

def rotate_chores_view(request):
    # Check if user is logged in and is admin
    if not request.session.get('user_id'):
        return redirect('login')
    
    if not request.session.get('is_admin'):
        return redirect('chore_assignments')
    
    # Execute the rotate chores command immediately
    from django.core.management import call_command
    from django.contrib import messages
    
    try:
        call_command('rotate_chores')
        messages.success(request, 'Chores rotated successfully!')
    except Exception as e:
        messages.error(request, f'Failed to rotate chores: {str(e)}')
    
    return redirect('chore_assignments')