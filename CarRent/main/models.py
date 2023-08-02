from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()
# Create your models here.


class Customer(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="cutomer_images/")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.id.username


class Garage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Garage")
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name + str(id)


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    seat = models.IntegerField(default=4)
    price = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)
    total_trips = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    current_city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)
    total_trips = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Rent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    total_price = models.IntegerField()
    feedback = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " " + self.car.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    review = models.TextField()

    def __str__(self):
        return self.user.username + " " + self.car.name


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_date = models.DateField()
    payment_amount = models.IntegerField()

    def __str__(self):
        return self.user.username + " " + self.rent.car.name
