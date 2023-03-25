from app.question.model import question
from app.question.serializer import QuestionSerializer
from datetime import datetime

class ExportQuestionController():
    def get(self):
        filters = {
        "approved_by_reviewer":"1",
        "approved_by_manager":"1",
        "published":"0",
        "exported_date__isnull":True
        }
        fields_to_update = {
            "published":"1",
            "exported_date":datetime.now()
        }
        all_qus = question.objects.filter(**filters, is_active=True)
        serializeobj = QuestionSerializer(all_qus, many=True)
        question.objects.filter(**filters).update(**fields_to_update)
        return serializeobj.data
