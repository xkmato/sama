from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from main.models import School, CommunityUnit, FeesStructure
from main.serializers import SchoolSerializer, CommunityUnitSerializer, FeesStructureSerializer


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
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CommunityUnitList(ListCreateAPIView):
    """
        This endpoint lists all Community Units with ``GET`` request and creates new community with ``POST`` request

        By making a ``GET`` you can view all community units. A community unit has the following attributes

        * **id** - The ID of the Community Unit (int) (readonly)
        * **name** - The NAME of the Community Unit (str)
    """
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
    queryset = FeesStructure.objects.all()
    serializer_class = FeesStructureSerializer

