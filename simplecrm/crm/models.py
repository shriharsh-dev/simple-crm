from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    STATUS_CHOICE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('lead', 'Lead'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link customer to a user
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='lead')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"  # Show owner in string representation


class Interaction(models.Model):
    TYPE_CHOICES = (
        ('call', 'Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link interaction to a user
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    notes = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.interaction_type} with {self.customer.first_name} {self.customer.last_name} on {self.date.strftime('%Y-%m-%d')}"
