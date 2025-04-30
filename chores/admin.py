from django.contrib import admin
from .models import ChoreGroup, Chore, Person, Days

# Register your models here.
admin.site.register(Chore)
admin.site.register(ChoreGroup)
admin.site.register(Person)
admin.site.register(Days)

