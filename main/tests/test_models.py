from django.test import TestCase

from main import models


class ModelTests(TestCase):
    def test_school_create_or_update_from_csv_row(self):
        row1 = ['Kamuli', '1234', 'Some Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
               '23', '47', '38', 'Urban', '12/4/2011']
        row2 = ['Kamuli', '1324', 'Some Other Name', '33', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
               '23', '57', '28', 'Rural', '10/4/2012']
        row3 = ['Kampala', '1432', 'Another Name', '33', '26', '13', '14', '400000', '500000', '600000', '200000',
                '24', '23', '59', '28', 'Rural', '6/6/2016']

        row4 = ['Kamuli', '1234', 'Updated Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
                '23', '47', '38', 'Urban', '12/4/2011']

        models.School.create_or_update_from_csv_row(row1)

        self.assertEqual(models.School.objects.count(), 1)

        school = models.School.objects.get(pk='1234')
        self.assertEqual(school.name, 'Some Name')

        self.assertEqual(models.FeesStructure.objects.count(), 1)
        self.assertEqual(school.fees, models.FeesStructure.objects.first())
        self.assertEqual(models.CommunityUnit.objects.count(), 1)
        self.assertEqual(school.community_unit, models.CommunityUnit.objects.get())

        models.School.create_or_update_from_csv_row(row2)
        models.School.create_or_update_from_csv_row(row3)
        models.School.create_or_update_from_csv_row(row4)

        self.assertEqual(models.School.objects.count(), 3)

        school = models.School.objects.get(pk='1234')
        self.assertEqual(school.name, 'Updated Name')
