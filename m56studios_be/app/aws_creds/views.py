from rest_framework.views import APIView
from app.aws_creds.controller import GetAwsCredsController
from common.django_utility import send_response
from app.decorators import validate_params
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class GetAWSCredsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        getAwsCredsControllerObj = GetAwsCredsController()
        response_data = []
        description = None
        try:
            response_data = getAwsCredsControllerObj.get_object()
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)