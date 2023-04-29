from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Auth_sms


class SmsSend(APIView):
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
            p_num = request.data["phone_number"]
        except KeyError:
            return Response({"message": "Bad Request"}, status=400)
        else:
            Auth_sms.objects.update_or_create(phone_number=p_num)
            return Response({"message": "OK"})


class CheckNumber(APIView):
    @swagger_auto_schema(
        operation_summary="phone_number 만 보내면 됨 (나중에 자세히 씀)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["phone_number", "auth_number"],
            properties={
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="전화번호"
                ),
                "auth_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="인증번호"
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
            result = Auth_sms.check_auth_number(p_num, a_num)
            if result:
                return Response({"message": "OK", "result": result})
            else:
                return Response({"message": "인증번호 틀림"}, status=400)
