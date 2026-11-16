"""Models for the Car Dealership application."""
from django.db import models


class CarMake(models.Model):
    """Car manufacturer."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Car model belonging to a make."""
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(default=2024)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    """Car dealership."""
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    """Customer review for a dealer."""
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)
    review = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True)
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(blank=True, null=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user_name} - {self.dealer.full_name}"
