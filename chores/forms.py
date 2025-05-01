from django import forms
from .models import Chore

class ChoreCompletionForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['completed']
