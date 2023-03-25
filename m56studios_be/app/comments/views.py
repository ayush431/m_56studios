from rest_framework.views import APIView
from app.comments.controller import CommentsController
from common.django_utility import send_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.decorators import validate_params, validate_dependent_id

commentsControllerObj = CommentsController()


class CommentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @validate_params(params=['comment'])
    @validate_dependent_id
    def post(self, request, qn_id):
        response_data = []
        description = None

        try:
            request.data["user"] = request.user.user_id
            request.data["qus"] = qn_id
            comment_data = commentsControllerObj.post(request)
            response_data.append(comment_data)
            exception_occured = False
            return response_data
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)
