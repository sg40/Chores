from django.db import models
from django.contrib.auth.hashers import make_password, check_password


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
    chore_group = models.ForeignKey(ChoreGroup, on_delete=models.CASCADE, related_name="chores")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    chore_group = models.ForeignKey(ChoreGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_users')

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class RotationLog(models.Model):
    rotation_time = models.DateTimeField()

    def __str__(self):
        return f"Rotation at {self.rotation_time}"
    