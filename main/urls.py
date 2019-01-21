from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from main.views import SchoolList, SchoolDetail, CommunityUnitList, CommunityUnitDetail

urlpatterns = [
    path('schools/', SchoolList.as_view()),
    path('schools/<int:pk>', SchoolDetail.as_view()),
    path('community_units/', CommunityUnitList.as_view()),
    path('community_units/<int:pk>', CommunityUnitDetail.as_view()),
    path('', get_swagger_view(title="Sama API"))
]

urlpatterns = format_suffix_patterns(urlpatterns)