from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Contact, ProductType, Destination, Product, CustomProduct, Lead
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
User = settings.AUTH_USER_MODEL
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

from django.forms.models import BaseInlineFormSet

class LeadInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(LeadInlineFormSet, self).__init__(*args, **kwargs)
        # Now we need to make a queryset to each field of each form inline
        self.queryset = ContentType.objects.filter(model__in=['contact', 'destination', 'product', 'customproduct'])
        # kwargs["queryset"] = ContentType.objects.filter(model__in=['contact', 'destination', 'product', 'customproduct'])
        


class LeadsContactInline(admin.TabularInline):
    model = Lead
    formset = LeadInlineFormSet
    extra = 1

class LeadsInline(GenericTabularInline):
    model = Lead
    extra = 1
    # exclude = ['contact']

class DestinationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'ville', )


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'start_date', 'destination', )
    list_display_links = ('id','destination' )
    list_per_page = 40
    save_as = True
    list_filter = ('start_date', )
    list_editable = ['start_date',]
    search_fields = ('id', 'destination')
    inlines = [LeadsInline]# a comenter pour KAHRABACENTER.com
    # exclude  = ['is_facility', 'old_price']
    # resource_class = ProductResource
    # form = ProductModelForm


class LeadAdmin(ImportExportModelAdmin):
    # responsabel
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(LeadAdmin, self).get_form(request, obj, **kwargs)
    #     if obj:
    #         form.base_fields['responsable'].queryset = User.objects.filter(id=request.user.id)
    #     return form
    # END responsabel



    list_display = ('id', 'status', 'content_type', )
    exclude = ('object_id',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model__in=['contact', 'destination', 'product', 'customproduct'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'commune', 'email', 'phone', 'big_client', 'email', )
    autocomplete_fields = ['commune']

    list_display_links = ('id','name' )
    search_fields = ('id', 'name', 'phone', 'commune')
    list_filter = ('big_client', )
    list_editable = ['big_client',]
    inlines = [LeadsContactInline]# a comenter pour KAHRABACENTER.com


admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Destination, DestinationAdmin)


