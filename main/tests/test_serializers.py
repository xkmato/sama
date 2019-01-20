from django.forms import model_to_dict
from django.test import TestCase

from main.models import School
from main.serializers import SchoolSerializer, CommunityUnitSerializer, FeesStructureSerializer


class SerializerTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        row = ['Test School', '1234', 'Some Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
               '23', '47', '38', 'Urban', '12/4/2011']
        self.school = School.create_or_update_from_csv_row(row)

        self.school_serializer = SchoolSerializer(instance=self.school)
        self.community_serializer = CommunityUnitSerializer(instance=self.school.community_unit)
        self.fees_serializer = FeesStructureSerializer(instance=self.school.fees)

    def test_serializers_contain_expected_fields(self):
        school_data = self.school_serializer.data
        community_data = self.community_serializer.data
        fees_data = self.fees_serializer.data

        self.assertEqual(set(school_data.keys()), {'id', 'name', 'community_unit', 'num_olevel_students',
                                                   'num_alevel_students', 'num_boarding_students','num_day_students',
                                                   'num_female_students', 'num_male_students', 'num_students',
                                                   'num_teachers','location', 'date_enrolled', 'fees'})
        self.assertEqual(set(community_data.keys()), {'id', 'name'})
        self.assertEqual(set(fees_data.keys()), {'boarding_s3', 'day_s3', 'boarding_s5', 'day_s5'})
