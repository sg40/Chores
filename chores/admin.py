from django.contrib import admin
from .models import ChoreGroup, Chore, RotationRule, Assignment

# Register your models here.
admin.site.register(Chore)
admin.site.register(ChoreGroup)
admin.site.register(RotationRule)
admin.site.register(Assignment)

