from django.contrib import admin
from .models import Contact, ProductType, Destination, Product, CustomProduct, Lead
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin


# class HasImages(SimpleListFilter):
#     title = "Photos" 
#     parameter_name ="pic"
#         # return Product.objects.filter(photos=True)
#     def lookups(self, request, model_admin):
#         return (
#             ('true', 'Avec Photos'),
#             ('false', 'Sans Photos')
#         )
#     def queryset(self, request, queryset):
#         if not self.value():
#             return queryset
#         if self.value().lower() == 'true':
#             return Product.objects.filter(photos__isnull=False)
#         elif self.value().lower() == 'false':
#             return Product.objects.filter(photos__isnull=True)



class LeadsInline(admin.TabularInline):
    model = Lead




class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'reference', 'name', 'category', 'price', 'price_24', 'price_12', 'price_48', 'price_60', 'price_72','new', 'top', 'actif', 'stock','to_home_page', 'order')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name' , 'reference')
    list_per_page = 40
    save_as = True
    list_filter = ('actif', 'is_pack',HasImages , 'new', 'to_home_page', 'category')
    list_editable = ['category', 'price', 'price_24', 'price_12', 'new', 'top', 'to_home_page','actif',  'stock', 'order']
    search_fields = ('id', 'name','reference','category__name', 'category__id')
    exclude  = ['is_facility', 'old_price']
    inlines = [PhotosLinesAdmin, AtributesValueInline,ProductDetailInline, ProductDocumentInline]# a comenter pour KAHRABACENTER.com
    resource_class = ProductResource
    form = ProductModelForm


