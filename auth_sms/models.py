# import requests
# from random import randint
# from django.db import models
# from common.models import CommonModel
# from django.utils import timezone
# import time
# import datetime
# from django.utils import timezone


# class Auth_sms(CommonModel):
#     phone_number = models.CharField(
#         verbose_name="휴대폰 번호", primary_key=True, max_length=11
#     )
#     auth_number = models.IntegerField(verbose_name="인증 번호", editable=False)

#     class Meta:
#         verbose_name_plural = "Auth_sms"

#     def save(self, *args, **kwargs):
#         self.auth_number = randint(1000, 10000)
#         super().save(*args, **kwargs)
#         self.send_sms()  # 인증번호가 담긴 SMS를 전송

#     def update(self, *args, **kwargs):
#         print

#     @classmethod
#     def check_auth_number(cls, p_num, c_num):
#         result = cls.objects.filter(phone_number=p_num, auth_number=c_num).exists()
#         if result:
#             return True
#         return False

#     def send_sms(self):
#         self.serviceId = "ncp:sms:kr:306207594347:curb-dev"
#         self.url = "https://sens.apigw.ntruss.com"
#         self.uri = f"/sms/v2/services/{self.serviceId}/messages"
#         self.timestamp = str(int(time.time() * 1000))
#         self.access_key = "B1EaHVNUwRPkQ3PTspyn"
#         signature = self.make_signature()
#         data = {
#             "type": "SMS",
#             "from": "01062848167",
#             "to": [self.phone_number],
#             "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number),
#             "messages": [{"to": self.phone_number}],
#         }
#         headers = {
#             "Content-Type": "application/json; charset=utf-8",
#             "x-ncp-apigw-timestamp": self.timestamp,
#             "x-ncp-iam-access-key": self.access_key,
#             "x-ncp-apigw-signature-v2": signature,
#         }
#         requests.post(self.url + self.uri, json=data, headers=headers)

#     def make_signature(self):
#         import base64
#         import hashlib
#         import hmac

#         secret_key = "XWYSYWDfx6HjptZBTR0wPcPvlv9NdNNgsYXZwgd7"  # secret key (from portal or Sub Account)
#         secret_key = bytes(secret_key, "UTF-8")

#         message = (
#             "POST" + " " + self.uri + "\n" + self.timestamp + "\n" + self.access_key
#         )
#         message = bytes(message, "UTF-8")
#         signingKey = base64.b64encode(
#             hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
#         )
#         return signingKey
