from rest_framework.views import APIView
from common.django_utility import send_response
from app.decorators import validate_params
from app.users.controller import UserController
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

userControllerObj = UserController()


class UserView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        response_data = []
        description = None
        try:
            user_data = userControllerObj.get(user_id, request)
            response_data = [user_data] if user_id else user_data
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)

    @validate_params(params=['first_name', 'last_name', 'email', 'password'])
    def post(self, request):
        response_data = []
        description = None
        try:
            user_data = userControllerObj.post(request)
            response_data.append(user_data)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)

    @validate_params(params=['first_name', 'last_name', 'email'])
    def put(self, request, user_id):
        response_data = []
        description = None
        try:
            court_data = userControllerObj.put(user_id, request)
            response_data.append(court_data)
            exception_occured = False
        except Exception as error_msg:
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, response_data=response_data)


class LoginView(APIView):
    @validate_params(params=['email', 'password'])
    def post(self, request):
        response_data = []
        header = {}
        description = None
        try:
            user_data, token = userControllerObj.post_login(request)
            response_data.append(user_data)
            header['auth-token'] = str(token.access_token)
            exception_occured = False
        except Exception as error_msg:
            token = None    
            description = error_msg
            exception_occured = True
        finally:
            return send_response(exception_occured=exception_occured, custom_description=description, request=request, header=header, response_data=response_data)
