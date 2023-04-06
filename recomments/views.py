from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ParseError


class Recomment(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        pass
