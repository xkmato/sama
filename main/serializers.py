from rest_framework import serializers

from main.models import School, CommunityUnit, FeesStructure


class FeesStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesStructure
        fields = ('boarding_s3', 'day_s3', 'boarding_s5', 'day_s5')


class SchoolSerializer(serializers.ModelSerializer):
    community_unit = serializers.ReadOnlyField(source='community_unit.name')
    fees = FeesStructureSerializer()

    class Meta:
        model = School
        fields = ('id', 'name', 'community_unit', 'num_olevel_students', 'num_alevel_students', 'num_boarding_students',
                  'num_day_students', 'num_female_students', 'num_male_students', 'num_students', 'num_teachers',
                  'location', 'date_enrolled', 'fees')


class CommunityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUnit
        fields = ('id', 'name')

