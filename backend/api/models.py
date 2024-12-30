from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)  # Make email unique
    full_name = models.CharField(max_length=100, null=False, blank=False)

    # Remove first_name and last_name
    first_name = None
    last_name = None

    def clean_full_name(self):
        if not self.full_name.strip():
            raise ValidationError("Full name cannot be blank.")

    def save(self, *args, **kwargs):
        # Ensure clean_full_name is called before saving
        self.clean_full_name()
        super().save(*args, **kwargs)
