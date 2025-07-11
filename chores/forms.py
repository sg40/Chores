from django import forms
from .models import Chore, Days, ChoreGroup

class ChoreCompletionForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['completed']

class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['name', 'description', 'days', 'chore_group']
        widgets = {
            'days': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }