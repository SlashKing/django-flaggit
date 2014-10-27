from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView

from . import utils
from .models import *
from .serializers import FlagSerializer, ReasonSerializer


User = get_user_model()

class CreateFlag(GenericAPIView):
    """
    Api to create a flag of an object app
    
    Args:
        app_model: (string) contain app name and it's model,
                   with format "appname.modelname"
        object_id: (integer) id of the object to be flagged
        comment : (string) additional comment from user
        reason_id : (string) predefined reason flag
        
    Returns:
        string "success" if successfully added to database,
        otherwise an array of errors will be shown
    """
    serializer_class = FlagSerializer

    def post(self, request, *args, **kwargs):

        serializer = FlagSerializer(data=request.DATA)

        if serializer.is_valid():
            errors = []
            # get new params app_model, object_id, ip, comment and reason
            params = serializer.object

            # get ip
            ip = utils.get_client_ip(request)

            # get comment
            comment = params.get('comment', '')

            # get content_type from "appname.modelname" and object id
            appname, modelname = params['app_model'].split('.')
            object_id = params.get('object_id')
            try :
                contenttype = ContentType.objects.get(app_label=appname, model=modelname)
                model = contenttype.model_class()
                obj = model.objects.get(id=object_id)
            except ContentType.DoesNotExist :
                errors.append("content type '%s.%s' does not exist" % (appname, modelname))
            except model.DoesNotExist:
                errors.append("No such %s object with id %s" % (model.__name__, object_id))

            # give the response
            if len(errors) > 0 :
                return Response({'errors':errors})
            else :
                flag_instance = utils.flag(obj, request.user, ip, comment)

                # get reason
                # ignore if reason does not exist
                reason_id = params.get('reason_id')
                if reason_id :
                    try :
                        reason = Reason.objects.get(id=reason_id)
                        flag_instance.reason = reason
                        flag_instance.save()
                    except Reason.DoesNotExist:
                        pass

                return Response('success')

        return Response(serializer.errors)


class RetrieveReason(ListAPIView):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
