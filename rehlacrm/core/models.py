from django.db import models

# Create your models here.



class Contact(models.Model):
    name = models.CharField(verbose_name="" , max_length=200)
    adress = models.CharField(verbose_name="" , max_length=200)
    phone= models.CharField(verbose_name="" , max_length=200)


class ProductType(models.Model):
    name = models.CharField(verbose_name="" , max_length=200)


class Destination(models.Model):
    ville = models.CharField(verbose_name="" , max_length=200)


class Product(models.Model):
    start_date = models.DateTimeField(verbose_name="", auto_now=False, auto_now_add=False)
    destination = models.ForeignKey(Destination, verbose_name="", on_delete=models.CASCADE)


class CustomProduct(models.Model):
    start_date = models.DateTimeField(verbose_name="", auto_now=False, auto_now_add=False)




class Lead(models.Model):
    class Status(models.TextChoices):
        RESERVED = "Reserved", "RESERVED"
        CONFIRMED = "Confirmed", "CONFIRMED"
        CANCELED = "Canceled", "CANCELED"
    contact = models.ForeignKey(Contact, verbose_name="", on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=50)

