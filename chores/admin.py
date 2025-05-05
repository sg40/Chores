from django.contrib import admin
from .models import ChoreGroup, Chore, Person, Days


class ChoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'chore_group')

# Register your models here.
admin.site.register(Chore, ChoreAdmin)
admin.site.register(ChoreGroup)
admin.site.register(Person)
admin.site.register(Days)
