from django.contrib import admin
from .models import Person, ChoreGroup, Chore, Day

# Register your models here.
admin.site.register(Person)
admin.site.register(Chore)
admin.site.register(Day)
admin.site.register(ChoreGroup)
