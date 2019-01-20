from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from main.models import School, CommunityUnit
from main.serializers import SchoolSerializer, CommunityUnitSerializer


class SchoolList(ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CommunityUnitList(ListCreateAPIView):
    queryset = CommunityUnit.objects.all()
    serializer_class = CommunityUnitSerializer


class CommunityUnitDetail(RetrieveUpdateDestroyAPIView):
    queryset = CommunityUnit.objects.all()
    serializer_class = CommunityUnitSerializer

