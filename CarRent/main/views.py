from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import Car, Driver, Rent, Review, Garage, User, Customer
from django.contrib import messages
from django.db.models import Q
from datetime import datetime


# Create your views here.
def update():
    today = datetime.today().date()
    rents = Rent.objects.all()
    for rent in rents:
        if rent.end_date < today:
            rent.is_returned = True
            rent.save()
            rent.car.is_available = True
            rent.car.save()
            rent.driver.status = True
            rent.driver.save()


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pass"]
        user = authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("home")
    return render(request, "auth/login.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["pass"]
        password2 = request.POST["confirm_pass"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect("register")
            else:
                user = User.objects.create_user(username, email)
                user.set_password(password)
                user.save()
                customer = Customer.objects.create(id=user)
                customer.save()
                return redirect("login")
    return render(request, "auth/register.html")


def home(request):
    update()
    cars = Car.objects.filter(is_available=True)
    cancel = False
    print("Yo")
    if request.method == "GET":
        print("Yo2")
        country = request.GET.get("country")
        state = request.GET.get("state")
        city = request.GET.get("city")
        print(country, state, city)

        if country:
            print("Yo3")
            cars = cars.filter(
                garage__country=country, garage__state=state, garage__city=city
            )
            cancel = True

    return render(request, "home/home.html", {"cars": cars, "cancel": cancel})


def carDetails(request, id):
    car = Car.objects.get(id=id)
    if request.method == "POST":
        start_date = request.POST["pickup_date"]
        end_date = request.POST["return_date"]
        total_price = request.POST["total_price"]

        driver = Driver.objects.filter(
            current_city=car.garage.city, status=True
        ).first()
        if driver:
            rent = Rent.objects.create(
                user=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                total_price=int(total_price),
                driver=driver,
            )
            rent.save()

            car.is_available = False
            car.total_trips += 1
            car.save()
            driver.status = False
            driver.total_trips += 1
            driver.save()
            print(car.is_available)

            return redirect("upCommingTrips")

    return render(request, "car_details.html", {"car": car})


def cancelTrip(request, id):
    rent = Rent.objects.get(id=id)
    rent.car.is_available = True
    rent.car.total_trips -= 1
    rent.car.save()

    rent.driver.status = True
    rent.driver.total_trips -= 1
    rent.driver.save()
    rent.delete()
    return redirect("upCommingTrips")


def upCommingTrips(request):
    if request.user.is_authenticated:
        upcomming = Rent.objects.filter(user=request.user, is_returned=False)
        return render(request, "upcommingtrip.html", {"upcomming": upcomming})
    else:
        return redirect("login")


def prevTrips(request):
    if request.user.is_authenticated:
        prev = Rent.objects.filter(user=request.user, is_returned=True)
        return render(request, "previous_trip.html", {"prev": prev})
    else:
        return redirect("login")


def review(request, id):
    if request.method == "POST":
        driver_rating = request.POST["driver_rating"]
        car_rating = request.POST["car_rating"]
        review = request.POST["feedback"]
        rent = Rent.objects.get(id=id)

        print(driver_rating, car_rating, review)
        review = Review.objects.create(
            rent=rent,
            user=rent.user,
            driver=rent.driver,
            car=rent.car,
            review=review,
        )
        review.save()
        driver = Driver.objects.get(id=rent.driver.id)
        driver.rating = (driver.rating + int(driver_rating)) / (driver.total_trips)
        driver.save()

        car = Car.objects.get(id=rent.car.id)
        car.rating = (car.rating + int(car_rating)) / (car.total_trips)
        car.save()

        rent.feedback = True
        rent.save()
        return redirect("prevTrips")

    return render(request, "review.html")


def cProfile(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.user)
        return render(request, "cprofile.html", {"customer": customer})
    else:
        return redirect("login")


def dProfile(request, id):
    if request.user.is_authenticated:
        driver = Driver.objects.get(id=id)
        return render(request, "dprofile.html", {"driver": driver})
    else:
        return redirect("login")
