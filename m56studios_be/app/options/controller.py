from datetime import datetime
from .serializer import OptionsSerializer
from .model import options
from common.constant import INVALID_REQUEST_TRY_AGAIN, ID_DOES_NOT_EXIST, INVALID_DATA_FOR_OPTIONS
import json

class OptionsController():
    def get_object(self, opt_id):
        try:
            return options.objects.get(pk=opt_id)
        except:
            raise Exception(ID_DOES_NOT_EXIST)

    def get(self, qn_id, opt_id=None):
        if opt_id:
            serializeobj = OptionsSerializer(self.get_object(opt_id))
        else:
            serializeobj = OptionsSerializer(
                options.objects.filter(qn_id=qn_id), many=True)
        return serializeobj.data

    def post(self, request=None):
        if self.check_request(request=request):
            return self.save_data(obj=OptionsSerializer(data=request.data))

    def validate_json(self, json_data):
        try:
            if isinstance(json_data, list):
                for each_dict in json_data:
                    json.loads(json.dumps(each_dict))
            else:
                raise Exception(INVALID_DATA_FOR_OPTIONS)
        except Exception as e:
            raise Exception(INVALID_DATA_FOR_OPTIONS)

    def put(self, qn_id, request=None):
        if self.check_request(request=request):
            options = request.data.get("options")
            options_data = self.get(qn_id=qn_id)
            option_array = []
            for opt in options:
                option_array.append(opt.get("opt_id"))
            for option_data in options_data:
                if option_data.get("opt_id") not in option_array:
                    self.delete(option_data.get("opt_id") )
            if options:
                self.validate_json(options)
            for option in options:
                optionObj = {
                    "option":option.get('option'),
                    "qn_id":qn_id,
                    "is_correct":option.get('is_correct'),
                    "opt_id":option.get('opt_id')
                }
                if option.get('opt_id') is None:
                    newOption = {
                        "option":option.get('option'),
                        "qn_id":qn_id,
                        "is_correct":option.get('is_correct')
                    }
                    self.save_data(obj=OptionsSerializer(data=newOption))
                if option.get('opt_id') is not None:
                    self.save_data(obj=OptionsSerializer(self.get_object(optionObj['opt_id'] ), data=optionObj))

    def delete(self, opt_id=None):
        return self.get_object(opt_id).delete()

    def check_request(self, request):
        if request and request.data:
            return True
        raise Exception(INVALID_REQUEST_TRY_AGAIN)

    def save_data(self, obj):
        if obj.is_valid(raise_exception=True):
            obj.save()
            return obj.data
