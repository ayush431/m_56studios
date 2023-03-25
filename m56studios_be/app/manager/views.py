from rest_framework.views import APIView
from app.manager.controller import ManagerController
from common.django_utility import send_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.decorators import validate_params, validate_dependent_id
from dateutil.parser import parse

managerControllerObj = ManagerController()


class ManagerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response_data = []
        description = None
        total_records = None
        try:
            filter_type = request.query_params.get('filter_type')
            start_date = parse(request.query_params.get('start_date'))
            end_date = parse(request.query_params.get('end_date'))

            response_data = managerControllerObj.get(filter_type, start_date, end_date)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)

class EditorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_params(params=['user_email', 'start_date', 'end_date', 'filter'])
    def post(self, request):
        response_data = []
        description = None
        total_records = None
        try:
            response_data = managerControllerObj.get_editor(request)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)


class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_params(params=['start_date', 'end_date', 'filter_type'])
    def post(self, request):
        response_data = []
        description = None
        total_records = None
        try:
            response_data = managerControllerObj.get_by_category(request)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)

class FlaggedQuestionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_params(params=['start_date', 'end_date'])
    def post(self, request):
        response_data = []
        description = None
        total_records = None
        try:
            start_date = parse(request.data.get('start_date'))
            end_date = parse(request.data.get('end_date'))
            response_data = managerControllerObj.get_flagged_questions(start_date, end_date)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)

