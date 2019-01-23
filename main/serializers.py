from rest_framework import serializers

from main.models import School, CommunityUnit, FeesStructure, DataCSV


class FeesStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesStructure
        fields = ('boarding_s3', 'day_s3', 'boarding_s5', 'day_s5')


class SchoolSerializer(serializers.ModelSerializer):
    community_unit = serializers.ReadOnlyField(source='community_unit.name')
    fees = FeesStructureSerializer()

    class Meta:
        model = School
        fields = ('id', 'name', 'community_unit', 'has_olevel', 'has_alevel', 'has_boarding', 'has_day', 'has_female',
                  'has_male', 'num_students', 'num_teachers', 'location', 'date_enrolled', 'fees')


class CommunityUnitSerializer(serializers.ModelSerializer):
    number_of_schools = serializers.SerializerMethodField()

    class Meta:
        model = CommunityUnit
        fields = ('id', 'name', 'number_of_schools')

    def get_number_of_schools(self, obj):
        return obj.schools.count()


class DataCSVSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.name')
    class Meta:
        model = DataCSV
        fields = ('uploaded_by', 'csv',)


class SummarySerializer(serializers.Serializer):
    ratio_o_level_to_a_level = serializers.FloatField()
    median_fees_s3_day = serializers.FloatField()
    median_fees_s3_boarding = serializers.FloatField()
    median_fees_s5_day = serializers.FloatField()
    median_fees_s5_boarding = serializers.FloatField()
    average_school_size = serializers.FloatField()
    teacher_student_ratio_urban = serializers.FloatField()
    teacher_student_ratio_rural = serializers.FloatField()
    teacher_student_ratio_peri_urban = serializers.FloatField()

