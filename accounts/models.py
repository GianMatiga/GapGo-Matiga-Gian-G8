from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        ADMIN = "admin", "Admin"

    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    contact_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True)

    def save(self, *args, **kwargs):
        # Superusers created with createsuperuser are always Admins.
        if self.is_superuser:
            self.role = self.Role.ADMIN
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def dashboard_url_name(self):
        return "accounts:admin_dashboard" if self.is_admin_role else "accounts:student_dashboard"

    def __str__(self):
        return self.username
