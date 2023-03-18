import time
import uuid

import razorpay
from pyfcm import FCMNotification
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response as InBuiltResponse

from backend.settings import RZ_ID, RZ_KEY, FCM_KEY
from core.models import Token, Notification
from core.serializers import NotificationSerializer

pagination = LimitOffsetPagination()



push_notification_service = FCMNotification(api_key=FCM_KEY)

def send_user_notification(user, title, body, image):
    notif = Notification()
    notif.user = user
    notif.title = title
    notif.body = body
    notif.image = image

    notif.save()

    notif_data = NotificationSerializer(notif, many=False).data
    message_title = notif_data.get('title')
    message_body = notif_data.get('body')
    message_image = notif_data.get('image')
    message_time = notif_data.get('created_at')


    result = push_notification_service.notify_single_device(registration_id=user.fcmtoken,
                                                               message_title=message_title,
                                                               message_body=message_body, data_message=
                                                               {'image': message_image},
                                                               extra_notification_kwargs={'image': message_image},
                                                               sound=True)
    print(result)


def new_token():
    token = uuid.uuid1().hex
    return token


def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user)
    return Response({'token': token})


class IsAuthenticatedUser(BasePermission):
    message = 'unauthenticated_user'

    def has_permission(self, request, view):
        return bool(request.user)


class Response(InBuiltResponse):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        # todo remove in prod
        time.sleep(3)

        super().__init__(data=data, status=status,
                       template_name=template_name, headers=headers,
                       exception=exception, content_type=content_type)


client = razorpay.Client(auth=(RZ_ID, RZ_KEY))
