from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from . import views, views_api

urlpatterns = [

     #page url
     path('list', views.BuildingListView.as_view(),
         name='list'),
     path('detail-page/<int:pk>', views.BuildingDetailView.as_view(),
         name='page-detail'),
     path('edit-page/<building_id>', views.BuildingEditPageView.as_view(),
          name='page-edit'),
     path('create-page', views.BuildingCreatePageView.as_view(),
          name='page-create'),

     #api for reactJS url
     path('location/generate/<str:lat>/<str:lon>', views_api.CRMLocationView.as_view(),
          name='location-generate'),
     path('building-category-list', views_api.BuildingCategoryView.as_view(),
          name='get-building-category-list'),
	path('create', views_api.BuildingCreateView.as_view(),
		name='building-create'),
	path('detail/<int:pk>', views_api.BuildingDetailView.as_view(),
		name='building-detail'),
	path('update/<int:pk>', views_api.BuildingUpdateView.as_view(),
		name='building-update'),
     path('photo/<int:building_id>', views_api.BuildingLogo.as_view(),
          name='photo-building'),
]
