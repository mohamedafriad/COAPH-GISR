from django.db import models
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
import datetime
from centres.models import Centre, Region, Province, Commune

NIVEAUX_SCOLAIRE=(
	(1, _('NON DETERMINE')),
	(2, _('SANS')),
	(3, _('PRIMAIRE')),
	(4, _('COLLEGIAL')),
	(5, _('SECONDAIRE')),
	(6, _('BACCALUAREAT')),
	(7, _('TECHNCIEN/DUT')),
	(8, _('UNIVERSITAIRE')),
)

SITUATION_PROFESSIONNELLE=(
	(1, _('RECHERCHE UN EMPLOI')),
	(2, _('EN ACTIVITE')),
	(3, _('EN FORMATION')),
	(4, _('AUTRE')),
)

COUVERTUTE_SOC_CHOIX=(
	(1, _('NON DETERMINE')),
	(2, _('SANS')),
	(3, _('RAMED')),
	(4, _('CNSS')),
	(5, _('CNOPS')),
	(6, _('CMR')),
	(7, _('CIMR')),
	(8, _('ASSURANCE')),
)

SEXE_CHOIX=(
    (1, _('Masculin')),
    (2, _('Féminin')),
)

SITUATION_FAM_CHOIX=(
    (1, _('NON DETERMINE')),
    (2, _('ENFANT')),
    (3, _('CELIBATAIRE')),
    (4, _('MARIE(E)')),
    (5, _('DIVORCE(E)')),
    (6, _('VEUF(VE)')),
)

EXP_MOIS=(
	(1, _('Janvier')),
  	(2, _('Février')),
  	(3, _('Mars')),
  	(4, _('Avril')),
  	(5, _('Mai')),
  	(6, _('Juin')),
  	(7, _('Juillet')),
  	(8, _('Aout')),
  	(9, _('Septembre')),
  	(10, _('Octobre')),
  	(11, _('Novembre')),
  	(12, _('Décembre')),
)

EXP_ANNEE=(
  (2018, 2018),
  (2019, 2019),
  (2020, 2020),
  (2021, 2021),
  (2022, 2022),
  (2023, 2023),
  (2024, 2024),
  (2025, 2025),
  (2026, 2026),
  (2027, 2027),
  (2028, 2028),
  (2029, 2029),
  (2030, 2030),
  (2031, 2031),
  (2032, 2032),
  (2033, 2033),
  (2034, 2034),
  (2035, 2035),
)

class Beneficiaire(models.Model):
    centre = models.ForeignKey(
        Centre,
        verbose_name = _('Centre'),
        related_name = 'beneficiaires',
        on_delete = models.SET_NULL,
        null = True
    )
    cin = models.CharField(_("CIN"), max_length=15, blank=True, null=True)
    acte = models.CharField(_("N° Acte de Naissance"), max_length=20, blank=True, null=True)
    cin_exp_mois = models.PositiveSmallIntegerField(_("Mois Exp CIN"), blank=True, null=True, choices=EXP_MOIS)
    cin_exp_annee = models.PositiveSmallIntegerField(_("Année Exp CIN"), blank=True, null=True, choices=EXP_ANNEE)
    nom_ar = models.CharField(_("Nom Arabe"), max_length=30)
    prenom_ar = models.CharField(_("Prénom Arabe"), max_length=30)
    nom_fr = models.CharField(_("Nom (fr)"), max_length=30, blank=True)
    prenom_fr = models.CharField(_("Prénom (fr)"), max_length=30, blank=True)
    sexe = models.PositiveSmallIntegerField(_("Sexe"), choices=SEXE_CHOIX)
    date_naissance = models.DateField(_("Date naissance"))
    age = models.IntegerField(_("Age"))
    lieu_naissance = models.CharField(_("Lieu naissance"), max_length=30, blank=True)
    nom_tuteur_ar = models.CharField(_("Nom Tuteur"), max_length=30, blank=True)
    cin_tuteur = models.CharField(_("CIN Tuteur"), max_length=15, blank=True)
    nom_mere = models.CharField(_("Nom Mère"), max_length=30, blank=True)
    cin_mere = models.CharField(_("CIN Mère"), max_length=15, blank=True)
    adresse_region = models.ForeignKey(
        Region,
        verbose_name = _('Région'),
        related_name = "beneficiaires",
        on_delete = models.SET_NULL,
        null = True
    )
    adresse_province = models.ForeignKey(
        Province,
        on_delete = models.SET_NULL,
        related_name = "beneficiaires",
        verbose_name = _("Province"),
        null=True
    )
    adresse_commune = models.ForeignKey(
        Commune,
        on_delete = models.SET_NULL,
        related_name = "beneficiaires",
        verbose_name = _("Commune"),
        null = True
    )
    adresse = models.CharField(_("Adresse"), max_length=300, blank=True)
    email = models.EmailField(_("Email"), null=True, blank=True)
    telephone = models.CharField(_("Téléphone"), max_length=320, blank=True)
    situation_fam = models.PositiveSmallIntegerField(_("Situation familliale"), blank=True, choices=SITUATION_FAM_CHOIX, null=True, default=1)
    couverture_soc = models.PositiveSmallIntegerField(_("Couverture Sociale"), blank=True, choices=COUVERTUTE_SOC_CHOIX, null=True, default=1)
    ramed = models.CharField(_("N° RAMED"), max_length=20, blank=True)
    ramed_exp_mois = models.PositiveSmallIntegerField(_("Mois Exp RAMED"), blank=True, null=True, choices=EXP_MOIS)
    ramed_exp_annee = models.PositiveSmallIntegerField(_("Année Exp RAMED"), blank=True, null=True, choices=EXP_ANNEE)
    profession = models.CharField(_("Profession"), max_length=20, blank=True)
    scolarite = models.PositiveSmallIntegerField(_("Niveau Scolaire"), blank=True, choices=NIVEAUX_SCOLAIRE, default=1)
    situation_prof = models.PositiveSmallIntegerField(_("Situation Socio Professionnelle"), blank=True, choices=SITUATION_PROFESSIONNELLE, default=1)
    attestation = models.CharField(_("Code Vérification Attestation"), max_length=300, blank=True)

    def __str__(self):
        nom_complet_cin = ""
        if self.cin:
            nom_complet_cin = "{} {} | {}".format(self.nom_ar, self.prenom_ar, self.cin)
        elif self.acte :
            nom_complet_cin = "{} {} | {}".format(self.nom_ar, self.prenom_ar, self.acte)
        return nom_complet_cin

    def clean(self):
        """
        Check for instances with null values in unique_together fields.
        """
        from django.core.exceptions import ValidationError
        if self.acte is None and self.cin is None:
            raise ValidationError(_("Veuillez renseigner la Cin (cas adulte) ou l'acte de naissance (cas enfant)"))
        elif self.cin is not None and Beneficiaire.objects.filter(cin=self.cin).exists():
            raise ValidationError(_("Le bénéficiaire avec la cin=%s est déjà enregistré") % self.cin)
        elif self.acte is not None and Beneficiaire.objects.filter(acte=self.acte).exists():
            raise ValidationError(_("Le bénéficiaire avec l'acte numéro=%s est déjà enregistré") % self.acte)
        else:
            pass

    def nom_complet(self):
        return "{} {}".format(self.nom_ar, self.prenom_ar)

    def get_age(self, date_calcul = datetime.date.today()):
        naissance = self.date_naissance
        if naissance:
            return date_calcul.year - naissance.year - ((date_calcul.month, date_calcul.day) < (naissance.month, naissance.day))
        else:
            return False

    @mark_safe
    def cin_valide(self):
        now_year = datetime.date.today().year
        now_month = datetime.date.today().month
        if self.cin_exp_annee and self.cin_exp_mois:
            if self.cin_exp_annee > now_year:
                return '<i class="fas fa-check-circle"></i>'
            elif self.cin_exp_annee < now_year :
                return '<i class="fas fa-times-circle"></i>'
            elif self.cin_exp_annee == now_year and self.cin_exp_mois > now_month:
                return '<i class="fas fa-check-circle"></i>'
            else:
                return '<i class="fas fa-times-circle"></i>'
        else:
            return '<i class="fas fa-question"></i>'
    cin_valide.short_description = _('Validité CIN')

    @mark_safe
    def ramed_valide(self):
        now_year = datetime.date.today().year
        now_month = datetime.date.today().month
        if self.ramed_exp_annee and self.ramed_exp_mois:
            if self.ramed_exp_annee > now_year:
                return '<i class="fas fa-check-circle"></i>'
            elif self.ramed_exp_annee < now_year :
                return '<i class="fas fa-times-circle"></i>'
            elif self.ramed_exp_annee == now_year and self.ramed_exp_mois > now_month:
                return '<i class="fas fa-check-circle"></i>'
            else:
                return '<i class="fas fa-times-circle"></i>'
        else:
            return '<i class="fas fa-question"></i>'
    ramed_valide.short_description = _('Validité RAMED')

    @mark_safe
    def afficher_type_handicaps(self):
        handicaps = self.handicaps.all()
        handi_count = self.handicaps.count()
        result = ''
        for handicap in handicaps:
            handi_count -=1
            result += '{}'.format(handicap.__str__())
            if handi_count > 0:
                result += ' و '
        return result
    afficher_type_handicaps.short_description = _("Handicaps")

    def save(self, *args, **kwargs):
        self.age = self.get_age()
        super(Beneficiaire, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Bénéficiaire")
        verbose_name_plural = _("Bénéficiaires")
        unique_together = ('cin', 'acte', 'date_naissance')

TYPEH_CHOIX = (
    (1, _('MOTEUR')),
    (2, _('MENTAL')),
    (3, _('VISUEL')),
    (4, _('AUDITIF')),
    (5, _('VOCAL')),
)

DEGRE_CHOIX = (
	(0, _('NON DEFINI')),
	(1, _('LEGER')),
    (2, _('MOYEN')),
    (3, _('PROFOND')),
)

DUREE_CHOIX = (
	(0, _('NON DEFINI')),
	(1, _('DEFINITIVE')),
    (2, _('NON DEFINITIVE')),
    (3, _('EVOLUTIVE')),
)

ASSISTANCE_CHOIX = (
    (1, _('OUI')),
    (2, _('NON')),
)

class Handicap(models.Model):
   beneficiaire = models.ForeignKey(
       Beneficiaire,
       on_delete = models.CASCADE,
       verbose_name = _("Bénéficiaire"),
       related_name = "handicaps"
    )
   type_h = models.PositiveSmallIntegerField(_("Type"), choices=TYPEH_CHOIX)
   degre = models.PositiveSmallIntegerField(_("Degré"), choices=DEGRE_CHOIX, default=0)
   duree = models.PositiveSmallIntegerField(_("Durée"), choices=DUREE_CHOIX, default=0)
   assistance = models.PositiveSmallIntegerField(_("Assistance"), choices=ASSISTANCE_CHOIX, default=2)
   description = models.CharField(_("Description"), max_length=30, blank=True)
   date_h = models.DateField(_("Date début"), blank=True, null=True)
   cause_h = models.CharField(_("Cause"), max_length=30, blank=True)
   appareille = models.BooleanField(_("Appareillé"), null=True, blank=True)
   type_appareil = models.CharField(_("Type Appareil"), max_length=200, blank=True)

   def __str__(self):
       return "{} {} {}".format(self.get_type_h_display(), self.get_degre_display(), self.get_duree_display())

   class Meta:
       verbose_name = _("Handicap")
       verbose_name_plural = _("Handicaps")
