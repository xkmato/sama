import codecs
import csv

from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from main.models import School, CommunityUnit, FeesStructure, Summary, DataCSV
from main.serializers import SchoolSerializer, CommunityUnitSerializer, FeesStructureSerializer, SummarySerializer, \
    DataCSVSerializer


class SchoolList(ListCreateAPIView):
    """
        This endpoint Lists Schools with GET requests, and Creates a new School with POST request

        By making a ``GET`` request you can list all the Schools. Each school has the following attributes

        * **id** - The ID of the School (int)
        * **name** - The NAME of the school (str)
        * **community_name** - The Community Unit Name in which the school belongs (str) (readonly)
        * **num_students** - The Number of students in the school (int)
        * **num_teachers** - The Number of teachers in the school (int)
        * **location** - The location of the school (str: RURAL, URBAN, PERI-URBAN)
        * **date_enrolled** - The date when the school was enrolled (date)
        * **fees** - The Fees Structure for the school (dict)

        By making a ``POST`` request, you can create a new School with the fields above
    """

    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(RetrieveUpdateDestroyAPIView):
    """
    This endpoint displays School Details

    By making a ``GET`` request you can view the school details. Each school has the following attributes

    * **id** - The ID of the School (int)
    * **name** - The NAME of the school (str) (readonly)
    * **community_name** - The Community Unit Name in which the school belongs (str)
    * **num_students** - The Number of students in the school (int)
    * **num_teachers** - The Number of teachers in the school (int)
    * **location** - The location of the school (str: RURAL, URBAN, PERI-URBAN)
    * **date_enrolled** - The date when the school was enrolled (date)
    * **fees** - The Fees Structure for the school (dict)

    By making a ``PUT`` request, you can edit the relevant School with the fields above

    By making a ``DELETE`` request, you delete the relevant school
    """

    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CommunityUnitList(ListCreateAPIView):
    """
        This endpoint lists all Community Units with ``GET`` request and creates new community with ``POST`` request

        By making a ``GET`` you can view all community units. A community unit has the following attributes

        * **id** - The ID of the Community Unit (int) (readonly)
        * **name** - The NAME of the Community Unit (str)
    """

    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = CommunityUnit.objects.all()
    serializer_class = CommunityUnitSerializer


class CommunityUnitDetail(RetrieveUpdateDestroyAPIView):
    """
        This endpoint displays the list of a Community Unit

        By making a ``GET`` you can view a community unit's details. A community unit has the following attributes

        * **id** - The ID of the Community Unit (int) (readonly)
        * **name** - The NAME of the Community Unit (str)

        By making a ``PUT`` request, you can edit the community unit

        By making a ``DELETE`` request you can delete the community unit
    """

    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = CommunityUnit.objects.all()
    serializer_class = CommunityUnitSerializer


class FeesStructureList(ListAPIView):
    """
        This endpoint lists all Fees Structures with ``GET`` request

        By making a ``GET`` you can view all community units. A community unit has the following attributes

        * **boarding_s3** - The amount paid by S3 BOARDING students (int)
        * **day_s3** - The amount paid by S3 DAY students (int)
        * **boarding_s5** - The amount paid by S5 BOARDING students (int)
        * **day_s5** - The amount paid by S5 DAY students (int)
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = FeesStructure.objects.all()
    serializer_class = FeesStructureSerializer


class SummaryDetail(APIView):
    """
    Relevant Summaries for the available data
    """
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        summary = Summary()
        serializer = SummarySerializer(summary, many=False)
        return Response(serializer.data)


class DataCSVViewSet(ModelViewSet):
    queryset = DataCSV.objects.all()
    serializer_class = DataCSVSerializer

    def perform_create(self, serializer):
        file = self.request.FILES.get('csv')
        reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
        for row in reader:
            School.create_or_update_from_csv_row(row)
        serializer.save(uploaded_by=self.request.user)
