from django.contrib.contenttypes.models import ContentType
from flaggit.models import Flag, FlagInstance

def flag(obj, user=None, ip=None, comment=None):
    flag, created = Flag.objects.get_or_create(
        object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj)
    )
    if user and not user.is_anonymous():
        flag_instance, created = FlagInstance.objects.get_or_create(
            flag=flag,
            user=user,
        )
    else:
        flag_instance, created = FlagInstance.objects.get_or_create(
            flag=flag,
            ip=ip
        )
    flag_instance.ip = ip
    flag_instance.comment = comment
    flag_instance.save()

    return flag_instance


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
