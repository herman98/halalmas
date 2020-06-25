from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path

from . import views
from . import views_api


urlpatterns = [
	#page url
	path('list', views.CRMCompanyListView.as_view(),
		name='list'),
	path('create-page', views.CRMCompanyCreatePage.as_view(),
		name='page-create'),
	path('edit-page/<int:pk>', views.CRMCompanyEditPage.as_view(),
		name='page-edit'),

	#api for reactJS url

	path('create', views_api.CompanyCreateView.as_view(),
		name='company-create'),

	path('detail/<int:pk>', views_api.CompanyDetailView.as_view(),
		name='company-detail'),

	path('update/<int:pk>', views_api.CompanyUpdateView.as_view(),
		name='company-update'),
	 
]
