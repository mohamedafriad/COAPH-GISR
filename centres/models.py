from django.db import models
from django.utils.translation import gettext as _
from agr.CHOICES_LISTS import *
from django.contrib.auth.models import Group
from django.conf import settings

MILIEU_CHOIX=(
    (1, _('Urbain')),
    (2, _('Rural')),
)

class Region(models.Model):
    nom = models.CharField(_('Nom'), max_length=300)
    nom_fr = models.CharField(_('Nom (fr)'), max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nom

    @staticmethod
    def autocomplete_search_fields():
        return ("nom__icontains", "nom_fr__icontains",)

    class Meta:
        verbose_name = _('Région')
        verbose_name_plural = _('Régions')


class Province(models.Model):
    nom = models.CharField(_('Nom'), max_length=300)
    nom_fr = models.CharField(_('Nom (fr)'), max_length=300, blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete = models.CASCADE,
        related_name = "provinces",
        verbose_name = _("Région")
    )

    def __str__(self):
        return self.nom

    @staticmethod
    def autocomplete_search_fields():
        return ("nom__icontains", "nom_fr__icontains",)

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')


class Commune(models.Model):
    nom = models.CharField(_('Nom'), max_length=300)
    nom_fr = models.CharField(_('Nom (fr)'), max_length=300, blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete = models.CASCADE,
        related_name = "communes",
        verbose_name = _("Région")
    )
    province = models.ForeignKey(
        Province,
        on_delete = models.CASCADE,
        related_name = "communes",
        verbose_name = _("Province")
    )
    milieu = models.PositiveSmallIntegerField(_('Milieu'), blank=True, null=True, choices=MILIEU_CHOIX, default=2)

    def __str__(self):
        return self.nom

    @staticmethod
    def autocomplete_search_fields():
        return ("nom__icontains", "nom_fr__icontains",)

    class Meta:
        verbose_name = _('Commune')
        verbose_name_plural = _('Communes')


class Centre(models.Model):
    nom = models.CharField(_('Nom'), max_length=200)
    region = models.ForeignKey(
        Region,
        verbose_name = _('Région'),
        related_name = "centres",
        on_delete = models.SET_NULL,
        null = True
    )
    province = models.ForeignKey(
        Province,
        verbose_name = _('Province'),
        related_name = "centres",
        on_delete = models.SET_NULL,
        null = True
    )
    commune = models.ForeignKey(
        Commune,
        verbose_name = _('Commune'),
        related_name = "centres",
        on_delete = models.SET_NULL,
        null = True
    )
    telephone = models.CharField(_('Téléphone'), max_length=10, blank=True)
    fax = models.CharField(_('Fax'), max_length=10, blank=True)
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    adresse = models.CharField(_('Adresse'), max_length=300, blank=True)
    gerant = models.OneToOneField(
        Group,
        verbose_name = _('Gérant'),
        related_name = "centres",
        on_delete = models.SET_NULL,
        null = True
    )
    latitude = models.FloatField(_("latitude"), blank=True, null=True)
    longitude = models.FloatField(_("longitude"), blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nom)

    class Meta:
        verbose_name = _('Centre')
        verbose_name_plural = _('Centres')
