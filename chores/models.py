from django.db import models

class ChoreGroup(models.Model):
    name = models.CharField(max_length=255)

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
    rotation_period_weeks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Rotate every {self.rotation_period_weeks} week(s)"


class Assignment(models.Model):
    assignee_name = models.CharField(max_length=255, blank=True)
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE, related_name='assignments')
    week_start_date = models.DateField()

    def __str__(self):
        return f"{self.assignee_name} - {self.chore.name} - {self.week_start_date}"

    
    

