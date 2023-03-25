from common.django_utility import send_response
from common.constant import *
from functools import wraps
from app.question.model import question
from .models import user_model

def validate_params(params):
    def inner_validate_params(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            try:
                if not args[0].data or not isinstance(args[0].data, dict):
                    raise TypeError
                for each_param in params:
                    if not each_param in args[0].data.keys():
                        raise KeyError
            except Exception as e:
                return send_response(exception_occured=True, custom_description=MISSING_PARAMETER, request=args[0])
            return function(request, *args, **kwargs)
        return wrap
    return inner_validate_params

def validate_dependent_id(function):
    def wrap(request, *args, **kwargs):
        try:
            if(kwargs.get("user_id") and kwargs.get("qn_id")):
            # Validate both params in question
                if not question.objects.filter(qn_id=kwargs.get("qn_id"), user_id=kwargs.get("user_id")).exists():
                    raise KeyError
            if(kwargs.get("user_id")):
                if not user_model.objects.filter(user_id=kwargs.get("user_id")).exists():
                    raise KeyError
                pass
        except Exception as e:
            return send_response(exception_occured=True, custom_description=INVALID_PARAMETER, request=args[0])
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap