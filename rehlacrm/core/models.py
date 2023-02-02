from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

# Create your models here.

CHAMBRE = [
        ('SN', 'Single'),
        ('DB', 'Double'),
        ('TR', 'Triple'),
    ]


class ProductType(models.Model):
    name = models.CharField(verbose_name="Label" , max_length=200)



class StatusVisa(models.Model):
    title = models.CharField(verbose_name="Label", max_length=150)

class Contact(models.Model):
    name = models.CharField(verbose_name="Nom et prénom" , max_length=200, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", max_length=254, blank=True, null=True)
    phone= models.CharField(verbose_name="Téléphone" , max_length=200)
    big_client = models.BooleanField(verbose_name="grand voyageur", default=False)
    passport     = models.FileField(upload_to="images/passport", max_length=100, blank=True, null=True)

    commune = models.ForeignKey("wilaya.Commune", verbose_name="Commune", on_delete=models.CASCADE, blank=True, null=True)
    adress = models.CharField(verbose_name="Adresse" , max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Destination(models.Model):
    ville = models.CharField(verbose_name="ville" , max_length=200)
    class Meta:
        verbose_name = "Déstination"
    def __str__(self):
        return self.ville



class Lead(models.Model):
    class Status(models.TextChoices):
        RESERVED = "Reserved", "RESERVED"
        CONFIRMED = "Confirmed", "CONFIRMED"
        CANCELED = "Canceled", "CANCELED"
    # contact = models.ForeignKey(Contact, verbose_name="", on_delete=models.CASCADE)
    contact      = models.ForeignKey(Contact, verbose_name="Contact", on_delete=models.CASCADE)
    status       = models.CharField(choices=Status.choices, max_length=50)
    room         = models.CharField(verbose_name="Chambre", choices=CHAMBRE, max_length=50, default='DB')
    price        = models.DecimalField(verbose_name="Tarif Single", max_digits=10, decimal_places=2, default=0)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='my_orders', verbose_name="Résponsable" ,blank=True ,null=True)
    visa_status =  models.ForeignKey(StatusVisa, on_delete=models.SET_NULL,  blank=True, null=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Type de Lead")
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')








    

class Product(models.Model):
    start_date = models.DateTimeField(verbose_name="Date de départ", auto_now=False, auto_now_add=False)
    return_date = models.DateTimeField(verbose_name="Date de départ", )
    places_number = models.IntegerField(verbose_name="PAX", default=0)
    single_price =models.DecimalField(verbose_name="Tarif Single", max_digits=10, decimal_places=2, default=0)
    double_price =models.DecimalField(verbose_name="Tarif Double", max_digits=10, decimal_places=2, default=0)
    tripl_price =models.DecimalField(verbose_name="Tarif Triple", max_digits=10, decimal_places=2, default=0)
    destination = models.ForeignKey(Destination, verbose_name="Déstination", on_delete=models.CASCADE)
    hotel        = models.CharField(verbose_name="hôtel", max_length=50, null=True, blank=True)
    product_type = models.ForeignKey(ProductType, verbose_name="Type De produit", on_delete=models.SET_NULL, null=True, blank=True)
    leads = GenericRelation(Lead)
    

class CustomProduct(models.Model):
    start_date = models.DateTimeField(verbose_name="Date de départ", auto_now=False, auto_now_add=False)
    product_type = models.ForeignKey(ProductType, verbose_name="Type De produit", on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey(Destination, verbose_name="Déstination", on_delete=models.CASCADE)
    leads = GenericRelation(Lead)



from django.dispatch import receiver
from django.db.models.signals import post_save



# @receiver(post_save, sender=Contact)
# def send_created_contact(sender, instance, created, **kwargs):
#     if created:
#         print('BEFORE SENDING THE EMAIAL')
#         instance.send_email()
#         print('AFTREERRRR SENDING THE EMAIAL')