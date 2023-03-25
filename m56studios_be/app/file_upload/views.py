from rest_framework.views import APIView
from common.django_utility import send_response
from app.file_upload.controller import FileUploadController
from app.decorators import validate_dependent_id
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

fileUploadControllerObj = FileUploadController() 

class UploadFileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_dependent_id
    def post(self, request, vendor_id, vendor_name):
        response_data = []
        description = None
        try:
            response_data = fileUploadControllerObj.post(vendor_id, vendor_name, request)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)