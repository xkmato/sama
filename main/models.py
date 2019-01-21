from statistics import median

from django.db import models
from django.db.models import Avg, Sum

from main.utils import date_from_str


class CommunityUnit(models.Model):
    """
    Model for community Unit
    """
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ('name',)


class School(models.Model):
    """
    Model for School
    """
    URBAN = 'urban'
    RURAL = 'rural'
    PERI_URBAN = "peri-urban"

    LOCATION_CHOICES = ((URBAN, 'URBAN'), (RURAL, 'RURAL'), (PERI_URBAN, 'PERI-URBAN'))

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    community_unit = models.ForeignKey(CommunityUnit, related_name="schools", on_delete=models.CASCADE)
    has_olevel = models.BooleanField()
    has_alevel = models.BooleanField()
    has_boarding = models.BooleanField()
    has_day = models.BooleanField()
    has_female = models.BooleanField()
    has_male = models.BooleanField()
    num_students = models.IntegerField()
    num_teachers = models.IntegerField()
    location = models.CharField(max_length=11, choices=LOCATION_CHOICES)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date_enrolled', )

    @classmethod
    def create_or_update_from_csv_row(cls, row):
        """
        Method to create or update school from a row in csv file
        :param row: Row from csv file
        :return: School
        """
        community_unit = row[0]
        _id = int(row[1])
        name = row[2]
        has_olevel = bool(row[3])
        has_alevel = bool(row[4])
        has_boarding = bool(row[5])
        has_day = bool(row[6])
        boarding_fees_s3 = row[7] if row[7].isdigit() else 0
        day_fees_s3 = row[8] if row[8].isdigit() else 0
        boarding_fees_s5 = row[9] if row[9].isdigit() else 0
        day_fees_s5 = row[10] if row[10].isdigit() else 0
        has_female = bool(row[11])
        has_male = bool(row[12])
        num_students = row[13] if row[13].isdigit() else 0
        num_teachers = row[14] if row[14].isdigit() else 0
        location = row[15]
        date_enrolled = row[16]

        community_unit, _ = CommunityUnit.objects.get_or_create(name=community_unit)
        school_exists = cls.objects.filter(id=_id).exists()
        if school_exists:
            cls.objects.filter(id=_id).update(name=name, community_unit=community_unit, has_olevel=has_olevel,
                                              has_alevel=has_alevel, has_boarding=has_boarding, has_day=has_day,
                                              has_female=has_female, has_male=has_male, num_students=num_students,
                                              num_teachers=num_teachers, location=location.upper(),
                                              date_enrolled=date_from_str(date_enrolled))
            school = cls.objects.get(id=_id)
        else:
            school = cls.objects.create(id=_id, name=name, community_unit=community_unit,
                                        has_olevel=has_olevel,
                                        has_alevel=has_alevel,
                                        has_boarding=has_boarding, has_day=has_day,
                                        has_female=has_female, has_male=has_male,
                                        num_students=num_students, num_teachers=num_teachers,
                                        location=location.upper(), date_enrolled=date_from_str(date_enrolled))

        FeesStructure.create_or_update(school=school, boarding_s3=int(boarding_fees_s3), day_s3=int(day_fees_s3),
                                     boarding_s5=int(boarding_fees_s5), day_s5=int(day_fees_s5))
        return school


class FeesStructure(models.Model):
    """
    Model for Fees Structure for each school
    """
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name='fees')
    boarding_s3 = models.IntegerField()
    day_s3 = models.IntegerField()
    boarding_s5 = models.IntegerField()
    day_s5 = models.IntegerField()

    @classmethod
    def create_or_update(cls, **kwargs):
        """
        Method to create or update fees structure from given kwargs
        :param kwargs: dict(**kwargs)
        :return: FeesStructure
        """
        school = kwargs.get('school')
        if cls.objects.filter(school=school).exists():
            kwargs.pop('school')
            cls.objects.filter(school=school).update(**kwargs)
        else:
            cls.objects.create(**kwargs)
        return cls.objects.get(school=school)


class Summary(object):
    """
    Class to hold aggregated summaries for the Summary API endpoint
    """
    def __init__(self):
        """
        Initiate summaries to object when object is iniatilized
        """
        self.get_avarage_school_size()
        self.get_median_fees()
        self.get_ratio_o_level_vs_a_level()
        self.get_teacher_student_ratios()

    def get_ratio_o_level_vs_a_level(self):
        """
        Ratio of O level to A level schools
        :return:
        """
        o_level = School.objects.filter(has_alevel=False, has_olevel=True).count()
        a_level = School.objects.filter(has_alevel=True, has_olevel=False).count()
        try:
            self.ratio_o_level_to_a_level = o_level/a_level
        except ZeroDivisionError:
            self.ratio_o_level_to_a_level = 0


    def get_median_fees(self):
        """
        median values for fees across all classes
        :return:
        """
        self.median_fees_s3_day = median(list(FeesStructure.objects.values_list('day_s3', flat=True)))
        self.median_fees_s5_day = median(list(FeesStructure.objects.values_list('day_s5', flat=True)))
        self.median_fees_s3_boarding = median(list(FeesStructure.objects.values_list('boarding_s3', flat=True)))
        self.median_fees_s5_boarding = median(list(FeesStructure.objects.values_list('boarding_s5', flat=True)))

    def get_avarage_school_size(self):
        """
        Average school size aggregated
        :return:
        """
        self.average_school_size = School.objects.aggregate(avg_school_size=Avg('num_students'))['avg_school_size']

    def get_teacher_student_ratios(self):
        """
        Ratio of teachers to students across all locations
        :return:
        """
        teachers_urban = School.objects.filter(location__iexact='urban').aggregate(teachers=Sum('num_teachers'))
        teachers_rural = School.objects.filter(location__iexact='rural').aggregate(teachers=Sum('num_teachers'))
        teachers_peri_urban = School.objects.filter(location__iexact='peri-urban').aggregate(teachers=
                                                                                            Sum('num_teachers'))
        students_urban = School.objects.filter(location__iexact='urban').aggregate(students=Sum('num_students'))
        students_rural = School.objects.filter(location__iexact='rural').aggregate(students=Sum('num_students'))
        students_peri_urban = School.objects.filter(location__iexact='peri-urban').aggregate(students=
                                                                                             Sum('num_students'))

        self.teacher_student_ratio_urban = teachers_urban.get('teachers', 1) /students_urban.get('students',1)
        self.teacher_student_ratio_rural = teachers_rural.get('teachers', 1) /students_rural.get('students',1)
        self.teacher_student_ratio_peri_urban = teachers_peri_urban.get('teachers', 1) \
                                                / students_peri_urban.get('students',1)
