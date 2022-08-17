from django.db import models
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from beneficiaires.models import Beneficiaire
from centres.models import Centre, Region, Province, Commune, Membre

NATURE_INDIV = 1
NATURE_COLLECT = 2
NATURE_PROJET=(
    (NATURE_INDIV, _('Individuel')),
    (NATURE_COLLECT, _('Collectif')),
)

FORME_AE = 1
FORME_PH = 2
FORME_SOC = 3
FORME_COOP = 4
FORME_AUTRE = 5
FORME_JURIDIQUE_CHOIX=(
    (FORME_AE, _('Auto-Entrepreneur')),
    (FORME_PH, _('RC/Personne Physique')),
    (FORME_SOC, _('Société')),
    (FORME_COOP, _('Coopérative')),
    (FORME_AUTRE, _('Autre')),
)

SECT_SERVICES = 1
SECT_COMMERCE = 2
SECT_INDUSTRIE = 3
SECT_AGRICULTURE = 4
SECT_ARTISANAT = 5
SECT_AUTRE = 6
SECTEUR_CHOIX=(
    (SECT_SERVICES, _('Services')),
    (SECT_COMMERCE, _('Commerce')),
    (SECT_INDUSTRIE, _('Industrie')),
    (SECT_AGRICULTURE, _('Agriculture')),
    (SECT_ARTISANAT, _('Artisanat')),
    (SECT_AUTRE, _('Autre')),
)

TYPES_PIECE_LOCAL=(
    (1, _('Propriété')),
    (2, _('Promesse de location')),
    (3, _('Contrat de location')),
    (4, _('Mise à disposition')),
    (5, _('Engagement')),
)

PIECE_CHOIX=(
    (True, _('Oui')),
    (False, _('Non')),
)

NATURE_TUTEUR=(
    (1, _('Bénéficiaire')),
    (2, _('Tuteur (Père)')),
    (3, _('Tuteur (Mère)')),
    (4, _('Autre')),
)
'''
class Structure(object):
    nom = models.CharField(_('Nom Structure'), max_length=500)


class Note(object):
    projet = models.ForeignKey()
'''

class Session(models.Model):
    titre = models.CharField(_('Titre'), max_length=500)
    date_ouverture = models.DateTimeField(_('Date Ouverture Session'))
    date_fermeture = models.DateTimeField(_('Date Fermeture Session'))
    ouverte = models.BooleanField(_('Session Ouverte'))

    def __str__(self):
        return self.titre

    def nb_projets(self):
        pass

    class Meta:
        verbose_name=_('Session')
        verbose_name_plural = _('Les Sessions')


class EtapeProjet(models.Model):
    nom = models.CharField(_('Etape'), max_length=50)
    ordre = models.PositiveSmallIntegerField(verbose_name=_('Ordre'), null=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = _('Etape Demande')
        verbose_name_plural = _('Etapes Demande')


class Projet(models.Model):
    centre = models.ForeignKey(
        Centre,
        verbose_name = _('Centre'),
        related_name = 'projets',
        on_delete = models.SET_NULL,
        null = True
    )
    #beneficiaires = models.ManyToManyField(
    #    Beneficiaire,
    #    verbose_name = _("Bénéficiaire"),
    #)
    beneficiaire = models.ManyToManyField(
        Beneficiaire,
        verbose_name = _("Bénéficiaire"),
        through = 'ExecuteurProjet'
    )
    #nature_tuteur = models.PositiveSmallIntegerField(_("Nature Tuteur"), blank=True, null=True, choices=NATURE_TUTEUR, default=1)
    intitule = models.CharField(_("Intitulé"), max_length=200)
    date_demande = models.DateField(_('Date demande'), null=True, blank=True)
    description = models.CharField(_("Description"), max_length=500, blank=True)
    montant_total = models.DecimalField(_("Montant Global"), decimal_places=2, max_digits=10)
    montant_demande = models.DecimalField(_("Montant Demandé"), decimal_places=2, max_digits=10)
    montant_contribution = models.DecimalField(_("Contribution Personnelle"), decimal_places=2, max_digits=10, default=0)
    secteur = models.PositiveSmallIntegerField(_("Secteur"), blank=True, null=True, choices=SECTEUR_CHOIX )
    forme_juridique = models.PositiveSmallIntegerField(_("Forme Juridique"), blank=True, null=True, choices=FORME_JURIDIQUE_CHOIX)
    nature = models.PositiveSmallIntegerField(_("Nature projet"), blank=True, null=True, choices=NATURE_PROJET, default=1)
    lieu_region = models.ForeignKey(
        Region,
        verbose_name = _("Région Implantation"),
        related_name = "projets",
        on_delete = models.SET_NULL,
        null = True
    )
    lieu_province = models.ForeignKey(
        Province,
        on_delete = models.CASCADE,
        related_name = "projets",
        verbose_name = _("Province Implantation")
    )
    lieu_commune = models.ForeignKey(
        Commune,
        on_delete = models.CASCADE,
        related_name = "projets",
        verbose_name = _("Commune Implantation")
    )
    lieu_adresse = models.CharField(_("Lieu Implantation"), max_length=20, default=_("Guelmim"))
    piece_cin = models.BooleanField(_("Copie CIN"), choices=PIECE_CHOIX, default=False)
    piece_ramed = models.BooleanField(_("Copie RAMED"), default=False, choices=PIECE_CHOIX)
    piece_certificat = models.BooleanField(_("Certificat Médical"), default=False, choices=PIECE_CHOIX)
    piece_engagement = models.BooleanField(_("Engagement"), default=False, choices=PIECE_CHOIX)
    piece_devis = models.BooleanField(_("Devis"), default=False, choices=PIECE_CHOIX)
    piece_local = models.BooleanField(_("Local"), default=False, choices=PIECE_CHOIX)
    piece_conv_accom = models.BooleanField(_("Convention accompagnement"), default=False, choices=PIECE_CHOIX)
    piece_conv_finan = models.BooleanField(_("Convention Financement"), default=False, choices=PIECE_CHOIX)
    num_cheque = models.CharField(_("Num Chèque"), max_length=20, blank=True, null=True)
    date_cheque = models.DateField(_('Date Chèque'), null=True, blank=True)
    date_lancement = models.DateField(_('Date lancement'), null=True, blank=True)
    etape = models.ManyToManyField(
        EtapeProjet,
        related_name = "projets",
        verbose_name = _('Etape'),
        blank = True,
        through = 'SuiviProjet'
    )
    session = models.ForeignKey(Session, related_name="projets", on_delete=models.SET_NULL, null=True, verbose_name=_("Session"))

    def __str__(self):
        return "{}".format(self.intitule)

    class Meta:
        verbose_name = _('Projet')
        verbose_name_plural = _('Projets')

    def get_montant_approuve(self):
        return self.montant_demande

    def dossier_est_complet(self):
        if self.piece_cin and self.piece_engagement and self.piece_certificat and self.piece_devis:
            return _("Oui")
        else:
            return _("Non")
    dossier_est_complet.short_description = _("Dossier Complet")

    def get_etape(self):
        ordre = ""
        if self.suivi.count():
            dates = [x.date_etap for x in self.suivi.all()]
            ordres = [x.etape.ordre for x in self.suivi.all()]
            max_dates = max(dates)
            max_ordre = max(ordres)
            etape = self.suivi.get(date_etap=max_dates, etape__ordre=max_ordre)
            ordre = etape.etape.nom
        else:
            ordre = ""
        return ordre
    get_etape.short_description = _("Etape")

    def get_etape_date(self):
        ordre = ""
        if self.suivi.count():
            dates = [x.date_etap for x in self.suivi.all()]
            ordres = [x.etape.ordre for x in self.suivi.all()]
            max_dates = max(dates)
            max_ordre = max(ordres)
            etape = self.suivi.get(date_etap=max_dates, etape__ordre=max_ordre)
            ordre = etape.date_etap
        else:
            ordre = ""
        return ordre
    get_etape_date.short_description = _("Date étape")

    def get_etape_commentaire(self):
        ordre = ""
        if self.suivi.count():
            dates = [x.date_etap for x in self.suivi.all()]
            ordres = [x.etape.ordre for x in self.suivi.all()]
            max_dates = max(dates)
            max_ordre = max(ordres)
            etape = self.suivi.get(date_etap=max_dates, etape__ordre=max_ordre)
            ordre = etape.commentaire
        else:
            ordre = ""
        return ordre
    get_etape_commentaire.short_description = _("Commentaire")

    def get_etape_avancement(self):
        avancement = 0
        if self.suivi.count():
            dates = [x.date_etap for x in self.suivi.all()]
            ordres = [x.etape.ordre for x in self.suivi.all()]
            max_dates = max(dates)
            max_ordre = max(ordres)
            etape = self.suivi.get(date_etap=max_dates, etape__ordre=max_ordre)
            avancement = etape.avancement
        return avancement
    get_etape_avancement.short_description = _("Avancement")

    @mark_safe
    def get_beneficiaires(self):
        data ="<ul>"
        for ben in self.porteur.all():
            data += "<li>"+ ben.beneficiaire.__str__() +"</li>"
        data += "</ul>"
        return data
    get_beneficiaires.allow_tags=True
    get_beneficiaires.short_description=_("Bénéficiaires")



COMMISSION_CHOIX = (
    (1, _('PROVINCIALE')),
    (2, _('REGIONALE')),
    (3, _('CENTRALE')),
)

DECISION_CHOIX = (
    (1, _('VALIDE')),
    (2, _('REJETE')),
    (3, _('A REFAIRE')),
)


class Avis(models.Model):
    projet = models.ForeignKey(
        Projet,
        on_delete = models.CASCADE,
        verbose_name = _("Projet"),
        related_name = "avis"
    )
    commission = models.PositiveSmallIntegerField(_("Commission"), choices=COMMISSION_CHOIX)
    date_avis = models.DateField(_('Date avis'))
    num_pv = models.CharField(_('Numéro PV'), blank=True, max_length=10, null=True)
    decision = models.PositiveSmallIntegerField(_("Décision"), choices=DECISION_CHOIX)
    note = models.PositiveSmallIntegerField(_("Note"), default=0)
    observation = models.CharField(_('Observation'), blank=True, max_length=700, null=True)
    montant_approuve = models.DecimalField(_('Montant approuvé'), decimal_places=2, max_digits=10,  blank=True, null=True)
    nbre_tranche = models.PositiveSmallIntegerField(_('Nombre tranches'), blank=True, null=True)

    def __str__(self):
        return "{} | {}".format(self.get_commission_display(), self.date_avis)

    class Meta:
        verbose_name = _('Avis')
        verbose_name_plural = _('Avis')


class Visite(models.Model):
    projet = models.ForeignKey(
        Projet,
        on_delete = models.CASCADE,
        verbose_name = _("Projet"),
        related_name = "visites"
    )
    date_visite = models.DateTimeField(_('Date visite'))
    observation = models.CharField(_('Observation'), blank=True, max_length=700, null=True)
    #numero= models.CharField(_('Numero'))

    def __str__(self):
        return "{}".format(self.date_visite)

    class Meta:
        verbose_name = _('Visite')
        verbose_name_plural = _('Visites')


class SuiviProjet(models.Model):
    projet = models.ForeignKey(
        Projet,
        related_name = 'suivi',
        on_delete = models.CASCADE,
        verbose_name = _('Projet')
    )
    etape = models.ForeignKey(
        EtapeProjet,
        related_name = 'suivi',
        on_delete = models.CASCADE,
        verbose_name = _('Etape')
    )
    date_etap = models.DateField(_('Date étape'), blank=True, null=True)
    avancement = models.PositiveSmallIntegerField(_('Avancement étape'), default=0, help_text="%")
    commentaire = models.CharField(_('Commentaire'), max_length=300, blank=True)

    def __str__(self):
        return "{}".format(self.etape.nom)

    class Meta:
        verbose_name = _('Etape Projet')
        verbose_name_plural = _('Etapes Projet')


class ExecuteurProjet(models.Model):
    projet = models.ForeignKey(
        Projet,
        related_name = 'porteur',
        on_delete = models.CASCADE,
        verbose_name = _('Projet')
    )
    beneficiaire = models.ForeignKey(
        Beneficiaire,
        related_name = 'porteur',
        on_delete = models.CASCADE,
        verbose_name = _('Bénéficiaire')
    )
    nature_tuteur = models.PositiveSmallIntegerField(_("Nature Tuteur"), blank=True, null=True, choices=NATURE_TUTEUR, default=1)
    nom_tuteur_ar = models.CharField(_("Nom Tuteur"), max_length=30, blank=True)
    cin_tuteur = models.CharField(_("CIN Tuteur"), max_length=15, blank=True)

    def __str__(self):
        if self.nature_tuteur == 1:
            return "{}".format(self.beneficiaire.__str__())
        else :
            return "{} | {}".format(self.nom_tuteur_ar, self.cin_tuteur)

    class Meta:
        verbose_name = _('Porteur Projet')
        verbose_name_plural = _('Porteurs Projet')


class Note(models.Model):
    projet = models.ForeignKey(
        Projet,
        related_name = 'notes',
        on_delete = models.CASCADE,
        verbose_name = _('Projet')
    )
    user = models.ForeignKey(
        User,
        related_name = 'notes',
        on_delete = models.SET_NULL,
        null = True
    )
    commission = models.PositiveSmallIntegerField(_("Commission"), choices=COMMISSION_CHOIX, default=1)
    note_profil = models.PositiveSmallIntegerField(_("Note Profil entrepreneurial"), default=0)
    note_viabilite = models.PositiveSmallIntegerField(_("Note Viabilité du projet"), default=0)
    note_finance = models.PositiveSmallIntegerField(_("Note Aspects financiers"), default=0)
    note_totale = models.PositiveSmallIntegerField(_("Note Totale"), default=0)