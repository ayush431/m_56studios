from django.db import models
import uuid
from app.question.model import question
from ..models import user_model

class comments(models.Model):
    cmt_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now=True)
    qus = models.ForeignKey(question, on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)

    @property
    def user_details(self):
        "Returns the user details."
        from app.users.controller import UserController
        return UserController().get(user_id=self.user_id)