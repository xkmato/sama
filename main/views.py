from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from main.models import School
from main.serializers import SchoolSerializer


class SchoolList(ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
