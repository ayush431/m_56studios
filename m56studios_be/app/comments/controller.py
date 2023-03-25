from .serializer import CommentsSerialiser
from .model import comments
from common.constant import INVALID_REQUEST_TRY_AGAIN, ID_DOES_NOT_EXIST, INVALID_DATA_FOR_OPTIONS
import json

class CommentsController():
    def get_object(self, cmt_id):
        try:
            return comments.objects.get(pk=cmt_id)
        except:
            raise Exception(ID_DOES_NOT_EXIST)

    def get(self, qn_id, cmt_id=None):
        if cmt_id:
            serializeobj = CommentsSerialiser(self.get_object(cmt_id))
        else:
            serializeobj = CommentsSerialiser(
                comments.objects.filter(qus=qn_id), many=True)
        return serializeobj.data

    def post(self, request=None):
        if self.check_request(request=request):
            return self.save_data(obj=CommentsSerialiser(data=request.data))

    def check_request(self, request):
        if request and request.data:
            return True
        raise Exception(INVALID_REQUEST_TRY_AGAIN)

    def save_data(self, obj):
        if obj.is_valid(raise_exception=True):
            obj.save()
            return obj.data
