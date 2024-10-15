from django.urls import path
from . import views

urlpatterns = [
        path('',views.fetch_distribution),
        path('zvakavanda/',views.toraZvakavanda),

]

