from rest_framework.views import APIView
from app.get_images.controller import GetImagesController
from common.django_utility import send_response
from app.decorators import validate_params
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import traceback

class GetImagesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @validate_params(params=['query_string'])
    def post(self, request):
        getImagesControllerObj = GetImagesController()
        response_data = []
        description = None
        try:
            getImagesControllerObj.image_type = request.data.get('image_type')
            getImagesControllerObj.query_string = request.data.get('query_string')
            image_link = getImagesControllerObj.google_search_t(getImagesControllerObj)
            response_data = image_link
            exception_occured = False
        except Exception as error_msg:
            print(traceback.format_exc())
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)