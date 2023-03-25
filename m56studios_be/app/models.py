from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class user_model(AbstractUser):
    class Types(models.TextChoices):
        EDITOR = "editor", "Editor"
        REVIEWER = "reviewer", "Reviewer"
        MANAGER = "manager", "Manager"
        SUPER_ADMIN = "super_admin", "Super_admin"

    base_type = Types.REVIEWER

    user_type = models.CharField(
        ("Type"), max_length=50, choices=Types.choices, default=base_type)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    email_valid = models.BooleanField(default=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
