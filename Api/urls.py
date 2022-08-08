from django.urls import path

from Api.views import ClothesPlanView, GetPlanWeatherIDView, GetAllWeatherPlanView, GetCitiesListView

urlpatterns = [
    path('<str:location>', ClothesPlanView.as_view()),
    path('get_plan/<int:pk>', GetPlanWeatherIDView.as_view()),
    path('get_all_plan/', GetAllWeatherPlanView.as_view()),
    path('get_city_list/', GetCitiesListView.as_view())
]
