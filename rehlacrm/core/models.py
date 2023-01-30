from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class Lead(models.Model):
    class Status(models.TextChoices):
        RESERVED = "Reserved", "RESERVED"
        CONFIRMED = "Confirmed", "CONFIRMED"
        CANCELED = "Canceled", "CANCELED"
    # contact = models.ForeignKey(Contact, verbose_name="", on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()



class Contact(models.Model):
    name = models.CharField(verbose_name="Nom et prénom" , max_length=200)
    adress = models.CharField(verbose_name="Adresse" , max_length=200)
    phone= models.CharField(verbose_name="Téléphone" , max_length=200)
    leads        = GenericRelation(Lead)

class ProductType(models.Model):
    name = models.CharField(verbose_name="Titre" , max_length=200)


class Destination(models.Model):
    ville = models.CharField(verbose_name="ville" , max_length=200)
    leads = GenericRelation(Lead)


class Product(models.Model):
    start_date = models.DateTimeField(verbose_name="Date de départ", auto_now=False, auto_now_add=False)
    destination = models.ForeignKey(Destination, verbose_name="Déstination", on_delete=models.CASCADE)
    leads = GenericRelation(Lead)

class CustomProduct(models.Model):
    start_date = models.DateTimeField(verbose_name="", auto_now=False, auto_now_add=False)



