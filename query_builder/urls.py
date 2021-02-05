from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainIndex.as_view(), name='main-index'),
    path('settings_select/', views.SettingsSelectView.as_view(),
         name='settings-select'),
    path('query_builder/', views.QueryBuilderView.as_view(), name='query-builder'),
]
