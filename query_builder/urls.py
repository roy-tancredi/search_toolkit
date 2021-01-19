from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainIndex.as_view(), name='main-index'),
    path('query_builder/', views.QueryBuilderView.as_view(), name='query-builder'),
]
