from django.contrib import admin
from .models import Centre, Region, Province, Commune
from agr.actions import export_as_xls
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

@admin.register(Centre)
class CentreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'province', 'commune', 'telephone', 'adresse', 'gerant', 'longitude', 'latitude')
    search_fields = ['nom', 'province', 'adresse']
    #autocomplete_fields = ['region', 'province', 'commune']
    actions = [export_as_xls]
    show_full_result_count = False
    view_on_site = False
    raw_id_fields = ("region", "province", "gerant")
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['region', 'province', 'gerant'],
    }
    list_editable = ('region', 'province', 'adresse')
    actions_on_top = True
    list_select_related = ('region', 'province', 'commune', 'gerant')

    # def get_queryset(self, request):
    #     qs = super(CentreAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(gerant__id=request.user.groups.get().id)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.is_superuser:
            return True
        elif request.user.groups.get().id == obj.gerant.id:
            return True
        else:
            return False

    def get_form(self, request, obj=None, **kwargs):
        form = super(CentreAdmin, self).get_form(request, obj, **kwargs)
        if 'gerant' in form.base_fields and not request.user.is_superuser:
            form.base_fields['gerant'].disabled = True
        return form

    #def get_fieldsets(self, request, obj=None):
    #    map_html = render_to_string("admin/includes/map.html")
    #    fieldsets = [
    #        (_("Main Data"), {"fields": ("nom", "gerant")}),
    #        (_("Contact"), {"fields": ("telephone", "fax", "email")}),
    #        (_("Addresses"), {"fields": ("region","province","commune", "adresse", "latitude", "longitude")}),
    #        (_("Map"), {"description": map_html,"fields": []}),
    #    ]
    #    return fieldsets

class ProvinceInline(admin.StackedInline):
    model = Province


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    inlines = [ProvinceInline]


class CommuneInline(admin.StackedInline):
    model = Commune

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'region')
    search_fields = ('nom',)
    list_filter = ('region',)
    #autocomplete_fields = ('region',)
    inlines = [CommuneInline]


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'region', 'province', 'milieu')
    list_editable = ( 'region', 'province', 'milieu')
    list_filter = ( 'region', 'province', 'milieu')
    #autocomplete_fields = ('region', 'province')
    search_fields = ('nom',)


class GroupAdmin(BaseGroupAdmin):
    save_as = True


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
