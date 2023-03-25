from app.question.model import question
from datetime import datetime
import json
import pytz

from uuid import UUID
from app.status.model import status_log
from app.utility.db_utility import performBatchOperation


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

class SuperAdminController():
    def export(self, exported_date = None):

        # Find all questions with status as Ready To Publish and exported_date=Null.
        # Update status of those questions and return response.
        unexported_questions = None
        if exported_date:
            unexported_questions = question.objects.filter(status=question.status_choice.PUBLISHED, exported_date__date=exported_date)
        else:
            unexported_questions = question.objects.filter(status=question.status_choice.READY_TO_PUBLISH, exported_date__isnull=True)
        
        sql_statements = []
        statement = '''INSERT INTO questions (qn_id, question_str, hint_image_url, difficulty_level, category, vendor_id, vendor_name, original_qn_id, options, updated_at, disabled) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}); \n'''
        if unexported_questions:
            for each_question in unexported_questions:
                sql_statements.append(statement.format(
                        each_question.qn_id,
                        each_question.question.replace("'", "\\'").replace('"', '\\"'),
                        each_question.resrc_url,
                        each_question.difficulty_level,
                        each_question.category,
                        each_question.vendor_id,
                        each_question.vendor_name,
                        each_question.original_qn_id,
                        json.dumps(each_question.options, cls=UUIDEncoder),
                        datetime.now(),
                        False,
                    ))
        if not exported_date:
            all_published_ques = question.objects.filter(status=question.status_choice.READY_TO_PUBLISH, exported_date__isnull=True)
            status_log_obj = []
            for each_question in all_published_ques:
                status_log_obj.append(status_log(old_status=each_question.status, new_status=question.status_choice.PUBLISHED, qn_id_id=each_question.qn_id, user_id=each_question.user_id))
            all_published_ques.update(status=question.status_choice.PUBLISHED, exported_date=datetime.now(tz=pytz.UTC))
            performBatchOperation(status_log, status_log_obj, 'create')
        return sql_statements
