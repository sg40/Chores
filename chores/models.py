from django.db import models

class Days(models.Model):
    name = models.CharField(max_length=9)  # e.g., "Monday"

    def __str__(self):
        return self.name

class ChoreGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Chore(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    days = models.ManyToManyField(Days)
    completed = models.BooleanField(default=False)  # Track whether the chore is completed

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=255)
    chore_group = models.ForeignKey(ChoreGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_people')

    def __str__(self):
        return self.name
