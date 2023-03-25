from datetime import datetime
from .serializer import QuestionSerializer
from .model import question
from ..models import user_model
from common.constant import INVALID_REQUEST_TRY_AGAIN, ID_DOES_NOT_EXIST
from app.options.controller import OptionsController
from app.users.controller import UserController
from app.status.controller import StatusController
from app.generate_thumbnail.controller import ThumbnailController
from app.status.model import status_log
from common.pagination import SetPagination
from django.db import transaction
from common.profane_words import checkProfanity
from app.utility.db_utility import performBatchOperation

optionsControllerObj = OptionsController()
paginator = SetPagination()
thumbnailController = ThumbnailController()


class QuestionController():

    def option_check(self, options, status, reason):
        all_options_str = ""
        option_set = set()
        for each_option in options:
            option_set.add(each_option['option'])
            str_each_option = str(each_option["option"])
            all_options_str += (str_each_option + " ")
            if len(str_each_option) > 30:
                status = question.system_checks.INVALID
                reason = "Option > 30 chars"

            if not str_each_option[0].isupper() and  not str_each_option[0].isdigit():
                status = question.system_checks.INVALID
                reason = "Option first char not upper case"
                
        if len(option_set) != len(options):
            status = question.system_checks.INVALID
            reason = "Duplicate option"
        return status, reason, all_options_str

    def question_check(self, questionObj, optionsObj, user_type, run_duplicate=True):
        system_check = question.system_checks.VALID
        reason = ""
        if len(questionObj["question"]) > 60:
            system_check =  question.system_checks.INVALID
            reason = "Question > 60 chars"
        if questionObj["question"][0] == "\"" or questionObj["question"][0] == "'":
            if not questionObj["question"][1].isupper() and not questionObj["question"][1].isdigit():
                system_check = question.system_checks.INVALID
                reason = "Question first char not upper case"
        else:
            if not questionObj["question"][0].isupper() and not questionObj["question"][0].isdigit():
                system_check = question.system_checks.INVALID
                reason = "Question first char not upper case"
        if run_duplicate:
            if question.objects.filter(original_qn_id=questionObj["original_qn_id"]).exists():
                system_check = question.system_checks.DUPLICATE
                reason = ""
        system_check, reason, all_options_str = self.option_check(optionsObj, system_check, reason)
        text_to_check = "{} {}".format(questionObj["question"], all_options_str)

        system_check, reason = checkProfanity(text_to_check, system_check, reason)
        questionObj["system_check"] = system_check
        questionObj["invalid_reason"] = reason
        return questionObj

    def run_status_checks(self, questionObj, optionsObj, user):
        if questionObj and 'qn_id' in questionObj:
            curr_org_question = self.get_object(questionObj["qn_id"])
            if  curr_org_question:
                questionObj["old_status"] = curr_org_question.status
            else:
                questionObj["old_status"] = questionObj["status"]    
        else:
            questionObj["old_status"] = questionObj["status"]
        user_type = user.user_type
        if user_type == user_model.Types.EDITOR:
            # Status changes for Editors
            if ((questionObj["system_check"] == question.system_checks.VALID 
                    or questionObj["system_check"] == question.system_checks.PROFANITY) and 
                    questionObj["qn_verified_by_editor"] and 
                    questionObj["ans_verified_by_editor"] and 
                    questionObj["status"] == question.status_choice.DRAFT):
                # Reset reviwer flags
                questionObj["img_rejected_by_reviewer"] = False
                questionObj["qn_rejected_by_reviewer"] = False
                questionObj["approved_by_reviewer"] = False
                questionObj["status"] = question.status_choice.FOR_REVIEW
                questionObj["qn_submitted_date"] = datetime.now().date()
            
            if (questionObj["system_check"] == question.system_checks.DUPLICATE and 
                    questionObj["should_overwrite"]):
                
                # Check if the actual question is either under review or draft
                actual_question = question.objects.filter(original_qn_id=questionObj["original_qn_id"], status__in=[question.status_choice.DRAFT, question.status_choice.FOR_REVIEW], system_check__in=[question.system_checks.VALID, question.system_checks.INVALID]).first()
                if actual_question:
                    # Reset reviwer flags
                    questionObj["img_rejected_by_reviewer"] = False
                    questionObj["qn_rejected_by_reviewer"] = False
                    questionObj["approved_by_reviewer"] = False
                    questionObj["status"] = question.status_choice.FOR_REVIEW
                    questionObj["system_check"] = question.system_checks.VALID
                    actual_question.system_check = question.system_checks.DUPLICATE
                    actual_question.status = question.status_choice.DISCARDED
                    actual_question.discarded_by_editor = True
                    questionObj["qn_submitted_date"] = datetime.now().date()
                    actual_question.save()
                    questionObj = self.question_check(questionObj, optionsObj, user_type, False)
                else: 
                    raise Exception("Cannot overrride question, question already approved or published")
            
            if questionObj["discarded_by_editor"] and questionObj["system_check"] == question.system_checks.DUPLICATE:
                questionObj["status"] = question.status_choice.DISCARDED
                questionObj["qn_submitted_date"] = datetime.now().date()

            if questionObj["rejected_by_editor"]:
                questionObj["status"] = question.status_choice.REJECTED_BY_EDITOR
                questionObj["qn_submitted_date"] = datetime.now().date()

            curr_ques = self.get_object(questionObj["qn_id"]) if "qn_id" in questionObj else None
            if curr_ques and curr_ques.rejected_by_editor and not questionObj["rejected_by_editor"] and curr_ques.status == question.status_choice.REJECTED_BY_EDITOR:
                questionObj["status"] = question.status_choice.DRAFT

        if user_type == user_model.Types.REVIEWER:
            # Status changes for Reviwers
            if questionObj["approved_by_reviewer"]:
                questionObj["status"] = question.status_choice.APPROVED
                questionObj["user_reviewed"] = user.user_id
                
            if questionObj["qn_rejected_by_reviewer"]:
                questionObj["status"] = question.status_choice.REJECTED_BY_EDITOR
                questionObj["user_reviewed"] = user.user_id

            if questionObj["img_rejected_by_reviewer"]:
                questionObj["status"] = question.status_choice.DRAFT
                questionObj["qn_verified_by_editor"] = False
                questionObj["ans_verified_by_editor"] = False
                questionObj["user_reviewed"] = user.user_id

        if user_type == user_model.Types.MANAGER:
            questionObj["qn_submitted_date"] = datetime.now().date()

        return questionObj

    def get_object(self, qn_id):
        try:
            return question.objects.get(pk=qn_id)
        except:
            raise Exception(ID_DOES_NOT_EXIST,qn_id)
    
    def get_qus_id_object(self, qn_id):
        try:
            return QuestionSerializer(question.objects.get(pk=qn_id)).data, True
        except:
            return qn_id, False

    def validate_options(self, request):
        options = request.data.get("options")
        right_answer = False
        for option in options:
            if option.get('is_correct'):
                right_answer = True
        if not right_answer:
            raise Exception("Right answer not found for question  {}".format(request.data.get("question")))
        if len(options) < 3 or len(options) >= 6:
                if request.data.get("category")== "TRUE OR FALSE":
                    if len(options) < 2:
                        raise Exception("Invalid number of options found for question  {}".format(request.data.get("question")))
                else:
                    raise Exception("Invalid number of options found for question  {}".format(request.data.get("question")))

    def get(self, qn_id=None, request=None):
        if qn_id:
            serializeobj = QuestionSerializer(self.get_object(qn_id))
            return serializeobj.data, None

        filters = {}
        exclude = {}
        is_active = True
        if request.query_params:
            if "search" in request.GET:
                filters['question__icontains'] = request.query_params.get('search')
            if "category" in request.GET:
                filters['category'] = request.query_params.get('category')
            if "difficulty_level" in request.GET:
                filters['difficulty_level'] = request.query_params.get(
                    'difficulty_level')
            if "system_check" in request.GET:

                if request.query_params.get("system_check") == "Rejected by Reviewer":
                    filters['img_rejected_by_reviewer'] = True
                else:
                    filters['system_check'] = request.query_params.get(
                            'system_check')
            if "status" in request.GET:
                if request.query_params.get('status') == 'Inactive':
                    is_active = False
                else:
                    filters['status'] = request.query_params.get(
                            'status')
            if "image_tagged" in request.GET:
                if int(request.query_params.get('image_tagged')) == 0:
                    filters['resrc_url__isnull'] = True
                else:
                    exclude['resrc_url__isnull'] = True
            if "user" in request.GET:
                filtered_user = UserController().get_object_by_email(request.query_params.get('user'))
                if filtered_user:
                    if request.user.user_type == user_model.Types.MANAGER:
                        filters['user_reviewed'] = filtered_user.user_id
                    else:
                        filters['user_id'] = filtered_user.user_id
            if "date" in request.GET:
                filters["qn_submitted_date"] = request.query_params.get(
                        'date')
            if "offline_content" in request.GET:
                filters["offline_content"] = request.query_params.get('offline_content')
        all_qus = question.objects.filter(**filters, is_active=is_active).exclude(**exclude)
        if request.query_params.get('page') == "-1":
            serializeobj = QuestionSerializer(all_qus, many=True)
        else:    
            serializeobj = QuestionSerializer(
                    paginator.paginate_queryset(all_qus, request), many=True)
        return serializeobj.data, None if qn_id else len(all_qus)

    def post(self, request=None):
        if self.check_request(request=request):
            self.question_check(request.data, request.data.get('options'), request.user.user_type)
            return self.save_data(obj=QuestionSerializer(data=request.data))

    def put(self, qn_id, request=None):
        with transaction.atomic():
            if self.check_request(request=request):
                questionObj = self.run_status_checks(request.data, request.data.get('options'), request.user)
                questionObj = self.question_check(questionObj, request.data.get('options'), request.user.user_type, False)
                StatusController().save_status_log(qn_id, questionObj, request.user.user_id)
                self.save_data(obj=QuestionSerializer(
                    self.get_object(qn_id), data=request.data))
                self.validate_options(request)
                if request.data.get('status') == question.status_choice.READY_TO_PUBLISH:
                    # TODO: Start create thumbnail operation
                    thumbnailController.perform(None, qn_id)
                optionsControllerObj.put(qn_id, request)
                return QuestionSerializer(self.get_object(qn_id)).data
    
    def bulkPut(self, request=None):
        if self.check_request(request=request):
            # Filter and update questions
            filter = {}
            exclude = {}
            if "reviewer" in request.data and request.data["reviewer"]:
                filter["user_reviewed__email"] = request.data["reviewer"]

            if "difficulty_level" in request.data and request.data["difficulty_level"]:
                filter["difficulty_level"] = request.data["difficulty_level"]

            if "category" in request.data and request.data["category"]:
                filter["category"] = request.data["category"]
                
            if "offline_content" in request.data:
                filter["offline_content"] = request.data["offline_content"]

            if "image_tagged" in request.data:
                if int(request.data['image_tagged']) == 0:
                    filter['resrc_url__isnull'] = True
                else:
                    exclude['resrc_url__isnull'] = True
            filter["status"] = question.status_choice.APPROVED
            if "curr_status" in request.data and request.data["curr_status"] and request.data["curr_status"] != None:
                filter["status"] = request.data["curr_status"]
                if "status" in request.data and request.data["status"] and request.data["status"] == request.data["curr_status"]:
                    raise Exception("INVALID STATUS PROVIDED - Cannot update to same status")

            if "status" in request.data and request.data["status"] in [question.status_choice.READY_TO_PUBLISH, question.status_choice.FOR_REVIEW]:
                status_log_obj = []
                serializeObj = QuestionSerializer(question.objects.filter(**filter).exclude(**exclude), many=True)
                for serialize_data in serializeObj.data:
                    status_log_obj.append(status_log(old_status=filter["status"], new_status=request.data["status"], qn_id_id=serialize_data["qn_id"], user_id_id=request.user.user_id))
                question.objects.filter(**filter).update(status=request.data["status"], qn_submitted_date=datetime.now().date())
                performBatchOperation(status_log, status_log_obj, 'create')
                if request.data.get('status') == question.status_choice.READY_TO_PUBLISH:
                    thumbnailController.perform(question.status_choice.READY_TO_PUBLISH, None)
            else:
                raise Exception("INVALID STATUS PROVIDED")
            return ""

    def delete(self, qs_id, qn_id=None):
        self.get_object(qn_id).delete()
        return self.get(qs_id=qs_id)

    def check_request(self, request):
        if request and request.data:
            return True
        raise Exception(INVALID_REQUEST_TRY_AGAIN)

    def save_data(self, obj):
        if obj.is_valid(raise_exception=True):
            obj.save()
            return obj.data
