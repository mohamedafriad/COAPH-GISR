from django.contrib import admin
from django.utils.translation import gettext as _
from django.db import models
from .models import Beneficiaire, Handicap
from centres.models import Centre
#Modification du titre du site
admin.site.index_title = _("Tableau de bord")
admin.site.site_header = _("Administration AGR")
admin.site.site_title = _("Gestion AGR")
"""
class BeneficiaireResource(resources.ModelResource):
    class Meta:
        model = Beneficiaire
"""

class HandicapInline(admin.StackedInline):
    model = Handicap
    extra = 0
    classes = ('grp-collapse grp-open',)

#from bootstrap_datepicker_plus.widgets import DatePickerInput
@admin.register(Beneficiaire)
class BeneficiaireAdmin(admin.ModelAdmin):
    #resource_class=BeneficiaireResource
    list_display = (
        'cin',
        'acte',
        'nom_ar',
        'prenom_ar',
        'date_naissance',
        'afficher_type_handicaps',
        'cin_valide',
        'ramed_valide',
    )
    list_filter = (
        'adresse_region',
        'adresse_province',
        'adresse_commune',
        'sexe',
        'situation_fam',
        'couverture_soc',
        'scolarite',
        'handicaps__type_h',
    )
    readonly_fields =('age',)
    #change_list_template = "admin/change_list_filter_sidebar.html"
    search_fields = ['cin', 'nom_ar', 'prenom_ar']
    save_on_top = True
    list_display_links = ('cin', 'acte')
    autocomplete_fields = ('adresse_region', 'adresse_province', 'adresse_commune', 'centre')
    inlines = [ HandicapInline,]
    fieldsets = (
        ('', {
            'classes':(),
            'fields': ('centre',)
        }),
        (_('Etat Civile'), {
        	'classes':(),
        	'fields':('cin', ('cin_exp_mois', 'cin_exp_annee'), 'acte', ('nom_ar', 'prenom_ar'), ('nom_fr', 'prenom_fr'), ('date_naissance', 'lieu_naissance', 'age'), 'sexe', ('nom_tuteur_ar', 'cin_tuteur'), ('nom_mere', 'cin_mere'), 'attestation')
        }),
        (_('Infos de Contact'), {
        	'classes':(),
        	'fields':('adresse_region', 'adresse_province', 'adresse_commune', 'adresse', ('telephone', 'email'))
        }),
        (_('Situation Sociale'), {
        	'classes':(),
        	'fields':('situation_fam', 'couverture_soc', 'ramed', ('ramed_exp_mois', 'ramed_exp_annee'), 'situation_prof', 'profession', 'scolarite')
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super(BeneficiaireAdmin, self).get_form(request, obj, **kwargs)
        if 'centre' in form.base_fields and not request.user.is_superuser:
            centre_obj = Centre.objects.get(gerant__id=request.user.groups.get().id)
            form.base_fields['centre'].initial = centre_obj
            form.base_fields['centre'].disabled = True
            form.base_fields['adresse_region'].initial = centre_obj.region.id
            form.base_fields['adresse_province'].initial = centre_obj.province.id
        return form
    """
        Set extra=0 for inlines if object already exists
    """
    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request):
            formset = inline.get_formset(request, obj)
            if obj:
                formset.extra = 0
            yield formset


@admin.register(Handicap)
class HandicapAdmin(admin.ModelAdmin):
    list_display = (
        'beneficiaire',
        'type_h',
        'degre',
        'duree',
        'assistance',
        'date_h',
        'appareille'
    )
    list_filter = (
        'type_h',
        'appareille',
        'beneficiaire__adresse_province',
        'beneficiaire__adresse_commune',
    )
    autocomplete_fields = ['beneficiaire',]