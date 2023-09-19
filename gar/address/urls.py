from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:objectId>/", views.query, name="query"),
    path("levels/<int:objectId>/<str:hierarchy>/", views.levels, name="levels"),
    path("<int:objectId>/<str:hierarchy>/<int:levelId>/", views.query_level, name="query_level"),
]