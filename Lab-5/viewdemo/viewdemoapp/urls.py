from django.conf.urls import url
from viewdemoapp import views


urlpatterns = [
url(r'^', views.HomePageView.as_view()),
]