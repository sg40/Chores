from django.db import models

DAYS_OF_WEEK = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
]

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return dict(DAYS_OF_WEEK)[self.name]

class Chore(models.Model):
    name = models.CharField(max_length=100)
    days = models.ManyToManyField(Day)  # The days this chore is done

    def __str__(self):
        return self.name
    
class ChoreGroup(models.Model):
    name = models.CharField(max_length=100)
    chores = models.ManyToManyField(Chore, blank=True)

    