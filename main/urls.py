from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from main.views import SchoolList, SchoolDetail, CommunityUnitList, CommunityUnitDetail, SummaryDetail, DataCSVViewSet

urlpatterns = [
    path('schools/', SchoolList.as_view(), name='schools'),
    path('schools/<int:pk>', SchoolDetail.as_view(), name='school'),
    path('community_units/', CommunityUnitList.as_view(), name='communities'),
    path('community_units/<int:pk>', CommunityUnitDetail.as_view(), name='community'),
    path('summary/', SummaryDetail.as_view(), name='summary'),
    path('upload_csv/', DataCSVViewSet.as_view({'get': 'list', 'post': 'create'}), name='upload_csv'),

    path('api-token-auth/', obtain_auth_token),

    path('rest-auth/', include('rest_auth.urls')),

    path('', get_swagger_view(title="Sama API"))
]

urlpatterns = format_suffix_patterns(urlpatterns)
