from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Category
from . import serializers


class Categories(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)

        if serializer.is_valid():
            feed = serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = serializers.CategorySerializer(
#             category,
#             many=True,
#         )
#         return Response(serializer.data)
