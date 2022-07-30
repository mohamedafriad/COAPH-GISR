from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Projet, Avis, SuiviProjet, ExecuteurProjet, EtapeProjet, Session
from centres.models import Centre

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display=('titre', 'date_ouverture', 'date_fermeture', 'ouverte')


@admin.register(EtapeProjet)
class EtapeProjetAdmin(admin.ModelAdmin):
    list_display=('nom', 'ordre')


class ExecuteurProjetInline(admin.StackedInline):
    model = ExecuteurProjet
    extra = 0
    autocomplete_fields = ['beneficiaire',]


class AvisInline(admin.StackedInline):
    model = Avis
    extra = 0


class SuiviProjetInline(admin.TabularInline):
    model = SuiviProjet
    extra = 0


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    inlines = [ExecuteurProjetInline, AvisInline, SuiviProjetInline]
    list_display = ('get_beneficiaires', 'date_demande', 'intitule', 'montant_demande', 'secteur', 'dossier_est_complet', 'date_lancement', 'get_etape', 'get_etape_date', 'get_etape_commentaire')
    filter_horizontal = ['beneficiaire',]
    list_filter = (
        'lieu_region',
        'lieu_province',
        'lieu_commune',
        'date_demande',
        'secteur',
    )
    autocomplete_fields = ['centre', 'lieu_region', 'lieu_province', 'lieu_commune']
    radio_fields = {
        'piece_cin': admin.HORIZONTAL,
        'piece_ramed': admin.HORIZONTAL,
        'piece_certificat': admin.HORIZONTAL,
        'piece_engagement': admin.HORIZONTAL,
        'piece_local': admin.HORIZONTAL,
        'piece_devis': admin.HORIZONTAL,
        'piece_conv_accom': admin.HORIZONTAL,
        'piece_conv_finan': admin.HORIZONTAL,
    }
    date_hierarchy = 'date_demande'
    fieldsets = (
        (_('Détails'), {
            'classes': (),
            'fields': (
                'centre', 'session', 'intitule', 'date_demande', 'description', 'secteur', 'nature'
            )
        }),
        (_('Implantation'), {
            'classes': (),
            'fields': (
                'lieu_region', 'lieu_province', 'lieu_commune', 'lieu_adresse'
            )
        }),
        (_('Finance'), {
            'classes': (),
            'fields': (
                'montant_total', 'montant_demande', 'montant_contribution'
            )
        }),
        (_('Pièces demandées'), {
            'classes': (),
            'fields': (
                'piece_cin', 'piece_ramed', 'piece_certificat', 'piece_engagement', 'piece_local', 'piece_devis', 'piece_conv_accom', 'piece_conv_finan'
            )
        }),
        (_("Infos d'exécution"), {
            'classes': (),
            'fields': (
                'forme_juridique', 'num_cheque', 'date_cheque', 'date_lancement'
            )
        }),
    )

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.is_superuser:
            return True
        elif request.user.groups.get().id == obj.centre.gerant.id:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.is_superuser:
            return True
        elif request.user.groups.get().id == obj.centre.gerant.id:
            return True
        else:
            return False

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjetAdmin, self).get_form(request, obj, **kwargs)
        if 'centre' in form.base_fields and not request.user.is_superuser:
            centre_obj = Centre.objects.get(gerant__id=request.user.groups.get().id)
            form.base_fields['centre'].initial = centre_obj
            form.base_fields['lieu_region'].initial = centre_obj.region
            form.base_fields['lieu_province'].initial = centre_obj.region
            form.base_fields['centre'].disabled = True
        return form
