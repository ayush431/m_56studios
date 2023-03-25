from .serializer import UserSerializer, UserUpdateSerializer
from ..models import user_model
from rest_framework_simplejwt.tokens import RefreshToken
from common.constant import ID_DOES_NOT_EXIST, INVALID_REQUEST_TRY_AGAIN, INCORRECT_PASSWORD, INCORRECT_USERNAME

class UserController():
    def get_object(self, user_id):
        try:
            return user_model.objects.get(pk=user_id)
        except:
            raise Exception(ID_DOES_NOT_EXIST)

    def get_object_by_email(self, email):
        try:
            return user_model.objects.get(email=email)
        except:
            raise Exception(ID_DOES_NOT_EXIST)

    def get(self, user_id=None, request=None):
        if user_id:
            serializeobj = UserSerializer(self.get_object(user_id))
        else:
            if request and "user_type" in request.GET:
                filters = {}
                filters["user_type"] = request.query_params.get("user_type")
                serializeobj = UserSerializer(user_model.objects.filter(**filters), many=True)
            else:
                serializeobj = UserSerializer(
                    user_model.objects.all(), many=True)
        return serializeobj.data

    def check_request(self, request):
        if request and request.data:
            return True
        raise Exception(INVALID_REQUEST_TRY_AGAIN)

    def save_data(self, obj):
        if obj.is_valid(raise_exception=True):
            obj.save()
            return obj.data
            
    def post(self, request=None):
        if self.check_request(request=request):
            return self.save_data(obj=UserSerializer(data=request.data))

    def put(self, user_id, request=None):
        if self.check_request(request=request):
            return self.save_data(obj=UserUpdateSerializer(self.get_object(user_id), data=request.data))

    def check_login_credentials(self, request):
        email = request.data['email']
        password = request.data['password']
        user = user_model.objects.filter(email=email).first()

        if user is None:
            raise Exception(INCORRECT_USERNAME)
        if not user.check_password(password):
            raise Exception(INCORRECT_PASSWORD)

        return  user

    def post_login(self, request):
        user = self.check_login_credentials(request)
        token = RefreshToken.for_user(user)
        user = UserSerializer(user_model.objects.filter(
            user_id=str(user.user_id)).first()).data

        return user, token


