from django.db import models
import uuid
from app.question.model import question
from common.utility import validate_capitalized

class options(models.Model):
    opt_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    option = models.CharField(max_length=254)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    qn_id = models.ForeignKey(question, on_delete=models.CASCADE)
