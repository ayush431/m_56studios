from rest_framework.views import APIView
from app.question.controller import QuestionController
from common.django_utility import send_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.decorators import validate_params, validate_dependent_id

questionControllerObj = QuestionController()


class QuestionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_dependent_id
    def get(self, request, qn_id=None):
        response_data = []
        description = None
        total_records = None
        try:
            question_data, total_records = questionControllerObj.get(qn_id, request)
            response_data = [question_data] if qn_id else question_data
            exception_occured = False
            return response_data
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)

    @validate_params(params=['question', 'resrc_url', 'original_url', 'cropped_json'])
    @validate_dependent_id
    def post(self, request):
        response_data = []
        description = None
        try:
            question_data = questionControllerObj.post(request)
            response_data.append(question_data)
            exception_occured = False
            return response_data
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)

    @validate_params(params=['question', 'resrc_url', 'original_url', 'cropped_json', 'options'])
    @validate_dependent_id
    def put(self, request, qn_id):
        response_data = []
        description = None
        try:
            question_data = questionControllerObj.put(qn_id, request)
            response_data.append(question_data)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)
            
    @validate_dependent_id
    def delete(self, request, qs_id, qn_id):
        response_data = []
        description = None
        try:
            response_data = questionControllerObj.delete(qs_id, qn_id)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)

class BulkQuestionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_params(params=['reviewer', 'status'])
    def put(self, request):
        response_data = []
        description = None
        try:
            question_data = questionControllerObj.bulkPut(request)
            response_data.append(question_data)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)