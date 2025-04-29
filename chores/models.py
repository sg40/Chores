from django.db import models
from django.contrib.auth.models import AbstractUser

class Household(models.Model):
    name = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=10, unique=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='households_created')

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_parent = models.BooleanField(default=False)
    household = models.ForeignKey(Household, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')

    def __str__(self):
        return self.username


class ChoreGroup(models.Model):
    name = models.CharField(max_length=255)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='chore_groups')

    def __str__(self):
        return self.name


class Chore(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    chore_group = models.ForeignKey(ChoreGroup, on_delete=models.CASCADE, related_name='chores')
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ])

    def __str__(self):
        return self.name


class RotationRule(models.Model):
    household = models.OneToOneField(Household, on_delete=models.CASCADE, related_name='rotation_rule')
    rotation_period_weeks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Rotate every {self.rotation_period_weeks} week(s)"


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name='assignments')
    week_start_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.chore.name} - {self.week_start_date}"

    
    

