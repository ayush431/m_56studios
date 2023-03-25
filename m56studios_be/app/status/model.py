from django.db import models
import uuid
from ..models import user_model
from app.question.model import question

class status_log(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    old_status = models.CharField(
        ("Type"), max_length=50, choices=question.status_choice.choices, null=True)
    new_status =  models.CharField(
        ("Type"), max_length=50, choices=question.status_choice.choices, null=True)
    user_id = models.ForeignKey(user_model, on_delete=models.CASCADE)
    qn_id = models.ForeignKey(question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def qn_with_tagged_images(self):
        from app.question.controller import QuestionController
        curr_qn = QuestionController().get(qn_id=self.qn_id_id)
        if curr_qn[0]["resrc_url"]:
            return 1
        else:
            return 0