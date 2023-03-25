from rest_framework.views import APIView
from app.generate_thumbnail.controller import ThumbnailController
from common.django_utility import send_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.decorators import validate_dependent_id

thumbnailControllerObj = ThumbnailController()


class GenerateThumbnailView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    #@validate_dependent_id
    def get(self, request):
        response_data = []
        description = None
        try:
            thumbnail_data = thumbnailControllerObj.perform(request.query_params.get('status'), request.query_params.get('qn_id'))
            response_data = thumbnail_data
            exception_occured = False
            return response_data
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)
