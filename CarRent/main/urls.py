from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("", views.home, name="home"),
    path("car-details/<int:id>", views.carDetails, name="carDetails"),
    path("upcomming-trips/", views.upCommingTrips, name="upCommingTrips"),
    path("past-trips/", views.prevTrips, name="prevTrips"),
    path("review/<int:id>", views.review, name="review"),
    path("customer-profile/", views.cProfile, name="cProfile"),
    path("driver-profile/<int:id>", views.dProfile, name="dProfile"),
    path("cancel-trip/<int:id>", views.cancelTrip, name="cancelTrip"),
]
