from django.db import models

from main.utils import date_from_str


class CommunityUnit(models.Model):
    name = models.CharField(max_length=60)


class School(models.Model):
    URBAN = 'urban'
    RURAL = 'rural'
    PERI_URBAN = "peri-urban"

    LOCATION_CHOICES = ((URBAN, 'URBAN'), (RURAL, 'RURAL'), (PERI_URBAN, 'PERI-URBAN'))

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    community_unit = models.ForeignKey(CommunityUnit, related_name="schools", on_delete=models.CASCADE)
    num_olevel_students = models.IntegerField()
    num_alevel_students = models.IntegerField()
    num_boarding_students = models.IntegerField()
    num_day_students = models.IntegerField()
    num_female_students = models.IntegerField()
    num_male_students = models.IntegerField()
    num_students = models.IntegerField()
    num_teachers = models.IntegerField()
    location = models.CharField(max_length=11, choices=LOCATION_CHOICES)
    date_enrolled = models.DateField(auto_now_add=True)

    @classmethod
    def create_or_update_from_csv_row(cls, row):
        community_unit, _id, name, num_olevel_students, num_alevel_students, num_boarding_students, num_day_students, \
         num_female_students, num_male_students, boarding_fees_s3, day_fees_s3, boarding_fees_s5, day_fees_s5, \
         num_students, num_teachers, location, date_enrolled = tuple(row)

        community_unit, _ = CommunityUnit.objects.get_or_create(name=community_unit)
        school_exists = cls.objects.filter(id=_id).exists()
        if school_exists:
            cls.objects.filter(id=_id).update(name=name, community_unit=community_unit,
                                              num_olevel_students=num_olevel_students,
                                              num_alevel_students=num_alevel_students,
                                              num_boarding_students=num_boarding_students,
                                              num_day_students=num_day_students,
                                              num_female_students=num_female_students,
                                              num_male_students=num_male_students,
                                              num_students=num_students, num_teachers=num_teachers,
                                              location=location.upper(), date_enrolled=date_from_str(date_enrolled))
            school = cls.objects.get(id=_id)
        else:
            school = cls.objects.create(id=_id, name=name, community_unit=community_unit,
                                        num_olevel_students=num_olevel_students,
                                        num_alevel_students=num_alevel_students,
                                        num_boarding_students=num_boarding_students, num_day_students=num_day_students,
                                        num_female_students=num_female_students, num_male_students=num_male_students,
                                        num_students=num_students, num_teachers=num_teachers,
                                        location=location.upper(), date_enrolled=date_from_str(date_enrolled))

        FeesStructure.create_or_update(school=school, boarding_s3=int(boarding_fees_s3), day_s3=int(day_fees_s3),
                                     boarding_s5=int(boarding_fees_s5), day_s5=int(day_fees_s5))
        return school


class FeesStructure(models.Model):
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name='fees')
    boarding_s3 = models.IntegerField()
    day_s3 = models.IntegerField()
    boarding_s5 = models.IntegerField()
    day_s5 = models.IntegerField()

    @classmethod
    def create_or_update(cls, **kwargs):
        school = kwargs.get('school')
        if cls.objects.filter(school=school).exists():
            kwargs.pop('school')
            cls.objects.filter(school=school).update(**kwargs)
        else:
            cls.objects.create(**kwargs)
        return cls.objects.get(school=school)
