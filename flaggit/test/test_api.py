import json

from django.test.testcases import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from ..models import Reason
from django.core.urlresolvers import reverse

User = get_user_model()
user_model = ''
if settings.AUTH_USER_MODEL :
    user_model = settings.AUTH_USER_MODEL.lower()
else :
    user_model = 'auth.user'


class TestAPI(TestCase):
    # use user model as an api

    def setUp(self):
        # create user to be flagged
        for i in range(10):
            User.objects.create(username="flag%d" % (i))

        # create flagger user
        User.objects.create(username="flagger")

        Reason.objects.create(title="some title", comment="some comment")

    def test_normal_create_flag(self):
        response = self.client.post(reverse('api_create_flag'), {'app_model': user_model,
                                                       'object_id': User.objects.get(username='flag1').pk,
                                                       'comment':'stoopid comment',
                                                       'reason_id':Reason.objects.all()[0].pk})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "success")

    def test_wrong_app(self):
        response = self.client.post(reverse('api_create_flag'), {'app_model': 'dummy.foo',
                                                       'object_id': User.objects.get(username='flag1').pk,
                                                       'comment':'stoopid comment',
                                                       'reason_id':Reason.objects.all()[0].pk})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "error")

    def test_retrieve_reason(self):
        response = self.client.get(reverse('api_retrieve_reason'))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 1)

    def test_wrong_reason(self):
        response = self.client.post(reverse('api_create_flag'), {'app_model': 'dummy.foo',
                                                       'object_id': User.objects.get(username='flag1').pk,
                                                       'reason_id': 20})
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "error")
