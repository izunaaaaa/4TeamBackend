from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response

# from .models import Auth_sms
from django.core.cache import cache
import requests
import time
from random import randint

import os
import environ

env = environ.Env()


class SmsSend(APIView):
    def send_sms(self):
        self.serviceId = os.environ.get("NCP_serviceID")
        self.url = "https://sens.apigw.ntruss.com"
        self.uri = f"/sms/v2/services/{self.serviceId}/messages"
        self.timestamp = str(int(time.time() * 1000))
        self.access_key = os.environ.get("NCP_accessKey")
        signature = self.make_signature()
        data = {
            "type": "SMS",
            "from": "01062848167",
            "to": [self.p_num],
            "content": "인증 번호 [{}]를 입력해주세요.".format(self.auth_number),
            "messages": [{"to": self.p_num}],
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": self.timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature,
        }
        requests.post(self.url + self.uri, json=data, headers=headers)

    def make_signature(self):
        import base64
        import hashlib
        import hmac

        secret_key = os.environ.get("NCP_secretKey")
        secret_key = bytes(secret_key, "UTF-8")

        message = (
            "POST" + " " + self.uri + "\n" + self.timestamp + "\n" + self.access_key
        )
        message = bytes(message, "UTF-8")
        signingKey = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )
        return signingKey

    @swagger_auto_schema(
        operation_summary="phone_number 만 보내면 됨 (나중에 자세히 씀)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone_number"],
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="전화번호"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
        },
    )
    def post(self, request):
        try:
            self.p_num = request.data["phone_number"]
        except KeyError:
            return Response({"message": "Bad Request"}, status=400)
        else:
            self.auth_number = randint(1000, 10000)
            self.send_sms()
            cache.set(self.p_num, self.auth_number, timeout=60 * 5)
            return Response({"message": "OK"})


class CheckNumber(APIView):
    @swagger_auto_schema(
        operation_summary="phone_number, auth_number 만 보내면 됨 (나중에 자세히 씀)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone_number", "auth_number"],
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="전화번호"
                ),
                "auth_number": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="인증번호"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
        },
    )
    def post(self, request):
        try:
            p_num = request.data["phone_number"]
            a_num = request.data["auth_number"]
        except KeyError:
            return Response({"message": "Bad Request"}, status=400)
        else:
            if cache.get(p_num) == a_num or str(cache.get(p_num)) == a_num:
                cache.delete(p_num)
                return Response({"message": "OK"})
            else:
                return Response({"message": "인증번호 틀림"}, status=400)
