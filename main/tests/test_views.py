from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from main.models import School, CommunityUnit, Summary
from main.views import SchoolList, CommunityUnitList, CommunityUnitDetail, SummaryDetail, SchoolDetail

factory = APIRequestFactory()


class ViewTests(TestCase):
    def setUp(self):
        row1 = ['Kamuli', '1234', 'Some Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
                '23', '47', '38', 'Urban', '12/4/2011']
        row2 = ['Kamuli', '1324', 'Some Other Name', '33', '24', '13', '14', '400000', '500000', '600000', '200000',
                '24',
                '23', '57', '28', 'Rural', '10/4/2012']
        row3 = ['Kampala', '1432', 'Another Name', '33', '26', '13', '14', '400000', '500000', '600000', '200000',
                '24', '23', '59', '28', 'Rural', '6/6/2016']

        row4 = ['Kamuli', '2134', 'Updated Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
                '23', '47', '38', 'Urban', '12/4/2011']

        row5 = ['Kamuli', '21341', 'Peri Name', '23', '24', '13', '14', '400000', '500000', '600000', '200000', '24',
               '23', '47', '38', 'peri-urban', '12/4/2011']

        School.create_or_update_from_csv_row(row1)
        School.create_or_update_from_csv_row(row2)
        School.create_or_update_from_csv_row(row3)
        School.create_or_update_from_csv_row(row4)
        School.create_or_update_from_csv_row(row5)

        self.user = User.objects.create(username='Test', email='test@test.test')
        self.factory = APIRequestFactory()

    def test_schools_list(self):
        request = factory.get(reverse("schools"))
        view = SchoolList.as_view()
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), School.objects.count())

    def test_communities_list(self):
        request = factory.get(reverse("communities"))
        view = CommunityUnitList.as_view()
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), CommunityUnit.objects.count())

    def test_school_detail(self):
        request = factory.get(reverse("school", args=[2134]))
        view = SchoolDetail.as_view()
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=2134)
        self.assertEqual(response.status_code, 200)
        results = response.data
        self.assertEqual(results['id'], 2134)

    def test_community_detail(self):
        community = CommunityUnit.objects.first()
        request = factory.get(reverse("community", args=[community.pk]))
        view = CommunityUnitDetail.as_view()
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=community.pk)
        self.assertEqual(response.status_code, 200)
        results = response.data
        self.assertEqual(results['id'], community.pk)
        self.assertEqual(results['name'], community.name)

    def test_summary_detail(self):
        summary = Summary()
        request = factory.get(reverse("summary"))
        view = SummaryDetail.as_view()
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data
        self.assertEqual(results['teacher_student_ratio_urban'], summary.teacher_student_ratio_urban)
        self.assertEqual(results['teacher_student_ratio_rural'], summary.teacher_student_ratio_rural)
        self.assertEqual(results['teacher_student_ratio_peri_urban'], summary.teacher_student_ratio_peri_urban)
        self.assertEqual(results['average_school_size'], summary.average_school_size)
        self.assertEqual(results['median_fees_s5_boarding'], summary.median_fees_s5_boarding)
        self.assertEqual(results['median_fees_s3_boarding'], summary.median_fees_s3_boarding)
        self.assertEqual(results['median_fees_s5_day'], summary.median_fees_s5_day)
        self.assertEqual(results['median_fees_s3_day'], summary.median_fees_s3_day)
