from django.contrib import admin
from .models import ChoreGroup, Chore, Household, User

# Register your models here.
admin.site.register(Chore)
admin.site.register(ChoreGroup)
admin.site.register(Household)
admin.site.register(User)

