from django.db import models


class Wilaya(models.Model):
    name = models.CharField(max_length=40, verbose_name="Wilaya", unique=True)
    mat = models.IntegerField(verbose_name='Matricule', blank=True,null=True)
    relai_delivery = models.DecimalField( max_digits=8, verbose_name="Livraison point de Relais", decimal_places=0, default=0)
    home_delivery = models.DecimalField( max_digits=10, verbose_name="Livraison à domicile", decimal_places=0, default=0)
    active = models.BooleanField(default=True, verbose_name="Livraison Active")
    
    class Meta:
        verbose_name = "Wilaya"
        verbose_name_plural = "1. Wilayas"

    def __str__(self):
        return self.name

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, verbose_name="Wilaya")
    name = models.CharField(max_length=50, verbose_name="Commune")
    # active = models.BooleanField(default=True, verbose_name="Livraison Active")
    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "2. Communes"  

    def __str__(self):
        return self.name
    @property
    def numero(self):
        return str(self.id)
        
