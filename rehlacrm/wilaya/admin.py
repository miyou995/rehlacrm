from django.contrib import admin
from .models import Commune, Wilaya
# Register your models here.
class CommuneAdmin(admin.ModelAdmin):
    list_display= ('name', 'wilaya')
    search_fields = ('id', 'name',)

admin.site.register(Commune, CommuneAdmin)


