from django.contrib import admin
from .models import ChoreGroup, Chore

# Register your models here.
admin.site.register(Chore)
admin.site.register(ChoreGroup)


