from rest_framework.views import APIView
from app.super_admin.controller import SuperAdminController
from common.django_utility import send_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from dateutil.parser import parse

superAdminController = SuperAdminController()


class SuperAdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response_data = []
        description = None
        total_records = None
        try:
            exported_date = None
            if request.query_params.get('exported_date'):
                exported_date = parse(request.query_params.get('exported_date'))

            response_data = superAdminController.export(exported_date)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, total_records=total_records, response_data=response_data)
