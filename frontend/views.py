from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from projets.models import Projet
from projets.models import FORME_AE, FORME_PH, FORME_SOC, FORME_COOP, FORME_AUTRE    # FORME JURIDIQUE
from projets.models import SECT_SERVICES, SECT_COMMERCE, SECT_INDUSTRIE, SECT_AGRICULTURE, SECT_ARTISANAT, SECT_AUTRE # SECTEUR ACTIVITE
from beneficiaires.models import Beneficiaire
from centres.models import Centre, Province, Region, Commune
from .forms import LoginForm
from projets.forms import ProjetForm


# view pour rediriger les requetes 404 vers la page d'accueil
def not_found_view(request):
    return redirect('front')

# view de la page d'accueil
def index(request):
    return render(request, template_name="frontend/index.html")

# view de la page espace perso de psh
# TODO : A REVOIR
def espace(request):
    return render(request, template_name="frontend/espace.html")

# view qui affiche la liste des coaph filtree par region/province
# TODO : ajout filtre commune
def centres(request):
    centres = Centre.objects.all()
    provinces = Province.objects.all()
    regions = Region.objects.all()
    province_selected = 0
    region_selected = 0
    try:
        region = int(request.GET['region'])
        if region != 0 :
            adresse_region = Region.objects.get(pk=region)
            centres=centres.filter(region=adresse_region)
            provinces = provinces.filter(region=adresse_region)
            region_selected = region
    except:
        pass
    try:
        province = int(request.GET['province'])
        if province != 0 :
            adresse_province = Province.objects.get(pk=province)
            centres=centres.filter(province=adresse_province)
            province_selected = province
    except:
        pass
    return render(request, template_name="frontend/centres.html", context={"centres": centres, "regions": regions, "provinces": provinces, "province_selected": province_selected, "region_selected": region_selected})

# view qui affiche la page détail du coaph
def centre(request, pk=None):
    centre = Centre.objects.get(pk=pk)
    return render(request, template_name="frontend/centre_map.html", context={"centre": centre})

# view qui affiche la page attestation
#def attestation(request):
#    return render(request, template_name="frontend/attestation.html")

#def suivi_attestation(request, demande=None):
#    return render(request, template_name="frontend/attestation_suivi.html")

# view qui affiche les informations et formalités des agr
# TODO: A revoir
def agr(request):
    return render(request, template_name="frontend/agr.html")

# view qui affiche les détails d'une demande agr
def suivi_agr(request):
    try:
        num_demande = request.GET['num_demande']
        projet = Projet.objects.get(pk=num_demande)
        projet_url = request.build_absolute_uri()
        #projet_url = str(website_url) + str(reverse('f-suivi-agr')) + '?num_demande='+ str(projet.pk)
        print(projet_url)
        return render(request, template_name="frontend/agr_suivi.html", context={"projet": projet, 'projet_url':projet_url})
    except:
        return render(request, template_name="frontend/agr_suivi.html", context={"error": True})

# view qui affiche les détails d'une demande agr :
# TODO : passer la template vers le dossier backend
def details_agr(request, num_demande=None):
    if request.user.is_authenticated:
        if num_demande :
            projet=Projet.objects.get(pk=num_demande)
            projet_url = request.build_absolute_uri()
            return render(request, template_name="frontend/agr_suivi.html", context={"projet": projet, 'projet_url':projet_url})
        else:
            projets=Projet.objects.all()
            return render(request, template_name="frontend/projets.html", context={"error": True, "projets": projets})
    else:
        return redirect('b-login')

# view de la page de connexion des membres de la commission
# TODO : eliminer la varible de session is_authenticated -> request.user.is_authenticated
def backlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                #request.session['is_authenticated'] = True
                return redirect('f-projets')
            else:
                request.session['loginError']=True
                return redirect('b-login')
        else:
            request.session['loginError']=True
            return redirect('b-login')
    else:
        return render(request, template_name="backend/login.html")

# view de la page de deconnexion des membres de la commission
# TODO : eliminer la varible de session is_authenticated
def backlogout(request):
    #request.session['is_authenticated'] = False
    logout(request)
    return redirect('front')

# view qui affiche la liste des projets filtree par region/province
# TODO : ajout filtre session + commune + etape + recherche par num_demande projet
# TODO : eliminer la varible de session is_authenticated -> request.user.is_authenticated
def list_projets(request):
    user = request.user
    if user.is_authenticated :  # cas d'un utilisateur autentifié
        region_selected = 0
        province_selected = 0
        commune_selected = 0
        demande = 0
        region_disabled = False
        province_disabled = False
        if user.is_superuser: # cas d'un administrateur ou la direction centrale
            regions = Region.objects.all()
            provinces = Province.objects.all()
            communes = Commune.objects.all()
            projets = Projet.objects.all()
            try:
                region = int(request.GET['region'])
                if region != 0:
                    lieu_region = Region.objects.get(pk=region)
                    projets=projets.filter(lieu_region=lieu_region)
                    provinces = provinces.filter(region=lieu_region)
                    communes = communes.filter(region=lieu_region)
                    region_selected = region
            except:
                pass
            try:
                province = int(request.GET['province'])
                if province != 0:
                    lieu_province = Province.objects.get(pk=province)
                    projets=projets.filter(lieu_province=lieu_province)
                    communes = communes.filter(province=lieu_province)
                    province_selected = province
            except:
                pass
            try:
                commune = int(request.GET['commune'])
                if commune != 0:
                    lieu_commune = Commune.objects.get(pk=commune)
                    projets=projets.filter(lieu_commune=lieu_commune)
                    commune_selected = commune
            except:
                pass
            try:
                demande = int(request.GET['num_demande'])
                if demande:
                    projets=projets.filter(pk=demande)
            except:
                pass
            region_disabled = False  # activation du champ region > form filtre par region/province/commune
            province_disabled = False # activation du champ province > form filtre par region/province/commune
            commune_disabled = False # activation du champ commune > form filtre par region/province/commune
            context = {
                "projets": projets,
                "regions": regions,
                "provinces": provinces,
                "communes": communes,
                "province_selected": province_selected,
                "region_selected": region_selected,
                "commune_selected": commune_selected,
                "region_disabled": region_disabled,
                "province_disabled": province_disabled,
                "commune_disabled": commune_disabled,
                "demande": demande,
            }
            return render(request, template_name="frontend/projets.html", context= context)
        else:  # cas d'un utilisateur normal (partenaire provincial/regional)
            region_selected = user.membre.region
            province_selected = user.membre.province
            regions = Region.objects.filter(pk=region_selected.pk)
            provinces = Province.objects.filter(region=region_selected)
            communes = Commune.objects.filter(region=region_selected)
            projets = Projet.objects.filter(lieu_region=region_selected)

            if province_selected:  # cas partenaire provincial
                projets=projets.filter(lieu_province=province_selected)
                provinces = Province.objects.filter(pk=province_selected.pk)
                communes = Commune.objects.filter(province=province_selected)
                region_disabled = True
                province_disabled = True
            else:    # cas partenaire régional
                region_disabled = True
                province_disabled = False
                try:
                    province = int(request.GET['province'])  # recherche si le champ province est rempli
                    if province != 0: # filtre par province
                        lieu_province = Province.objects.get(pk=province)
                        projets=projets.filter(lieu_province=lieu_province)
                        provinces = Province.objects.filter(region=region_selected)
                        communes = Commune.objects.filter(province=province_selected)
                        province_selected = province
                except:
                    pass
            try: # filtre par commune
                commune = int(request.GET['commune'])
                if commune != 0:
                    lieu_commune = Commune.objects.get(pk=commune)
                    projets=projets.filter(lieu_commune=lieu_commune)
                    commune_selected = commune
            except:
                pass
            try:   # filtre par numero demande
                demande = int(request.GET['num_demande'])
                if demande:
                    projets=projets.filter(pk=demande)
            except:
                pass
            # construction du dictionnaire des variables > template
            context = {
                "projets": projets,
                "regions": regions,
                "provinces": provinces,
                "communes": communes,
                "region_selected": region_selected,
                "province_selected": province_selected,
                "commune_selected": commune_selected,
                "region_disabled": region_disabled,
                "province_disabled": province_disabled,
                "demande": demande,
            }
            return render(request, template_name="frontend/projets.html", context= context)
    else:
        return redirect('b-login')


# view de la page qui affiche la liste des bénéficiaires
# TODO : completer la view
def list_psh(request):
    if request.user.is_authenticated :
        psh = Beneficiaire.objects.all()
        return render(request, template_name="frontend/psh.html", context={'psh': psh})
    else:
        return redirect('b-login')

# view qui affiche la page du tableau de bord -> donnees filtree par region/province
# TODO : ajout filtre par session + commune + etape
def dashboard(request):
    user = request.user
    if user.is_authenticated : # utilisateur authentifié
        province = 0
        region = 0
        projets_individuels = 0
        projets_collectifs = 0
        projets = Projet.objects.all()
        provinces = Province.objects.all()
        regions = Region.objects.all()
        region_selected = 0
        province_selected = 0
        region_disabled = False
        province_disabled = False
        if user.is_superuser:  # cas administrateur
            try:
                region = int(request.GET['region'])
                if region != 0:
                    lieu_region = Region.objects.get(pk=region)
                    projets=projets.filter(lieu_region=lieu_region)
                    provinces = provinces.filter(region=lieu_region)
                    region_selected = region
            except:
                pass
            try:
                province = int(request.GET['province'])
                if province != 0:
                    lieu_province = Province.objects.get(pk=province)
                    projets=projets.filter(lieu_province=lieu_province)
                    province_selected = province
            except:
                pass
        else:
            region_selected = user.membre.region
            province_selected = user.membre.province
            regions = Region.objects.filter(pk=region_selected.pk)
            provinces = Province.objects.filter(region=region_selected)
            communes = Commune.objects.filter(region=region_selected)
            projets = projets.filter(lieu_region=region_selected)

            if province_selected:  # cas partenaire provincial
                projets=projets.filter(lieu_province=province_selected)
                provinces = Province.objects.filter(pk=province_selected.pk)
                communes = communes.filter(province=province_selected)
                region_disabled = True
                province_disabled = True
            else:    # cas partenaire régional
                try:
                    province = int(request.GET['province'])  # recherche si le champ province est rempli
                    if province != 0: # filtre par province
                        lieu_province = Province.objects.get(pk=province)
                        projets=projets.filter(lieu_province=lieu_province)
                        provinces = Province.objects.filter(region=region_selected)
                        communes = communes.filter(province=province_selected)
                        province_selected = province
                        region_disabled = True
                        province_disabled = False
                except:
                    pass


        # TODO: nbre projets filtres par etape
        # nbre projets filtres par forme juridique : OK
        projets_ae = projets.filter(forme_juridique=FORME_AE).count()
        projets_ph = projets.filter(forme_juridique=FORME_PH).count()
        projets_soc = projets.filter(forme_juridique=FORME_SOC).count()
        projets_coop = projets.filter(forme_juridique=FORME_COOP).count()
        # nb projets filtres par milieu : OK
        projets_urbain = projets.filter(lieu_commune__milieu=1).count()
        projets_rural = projets.filter(lieu_commune__milieu=2).count()
        # TODO: nb projets filtres par secteur d'activite
        projets_commerce = projets.filter(secteur=SECT_COMMERCE).count()
        projets_services = projets.filter(secteur=SECT_SERVICES).count()
        projets_artisanat = projets.filter(secteur=SECT_ARTISANAT).count()
        projets_agriculture = projets.filter(secteur=SECT_AGRICULTURE).count()
        projets_industrie = projets.filter(secteur=SECT_INDUSTRIE).count()
        projets_autre = projets.filter(secteur=SECT_AUTRE).count()
        # empaquetage des valeurs qui seront affichees sur le tableau de bord
        dict_context ={
            "projets": projets,
            "regions": regions,
            "provinces": provinces,
            "province_selected": province_selected,
            "region_selected": region_selected,
            "region_disabled": region_disabled,
            "province_disabled": province_disabled,
            "projets_ae": projets_ae,
            "projets_ph": projets_ph,
            "projets_soc": projets_soc,
            "projets_coop": projets_coop,
            "projets_urbain":projets_urbain,
            "projets_rural": projets_rural,
            "projets_collectifs": projets_collectifs,
            "projets_commerce": projets_commerce,
            "projets_services": projets_services,
            "projets_artisanat": projets_artisanat,
            "projets_agriculture": projets_agriculture,
            "projets_industrie": projets_industrie,
            "projets_autre": projets_autre,
        }
        return render(request, template_name="backend/dashboard.html", context=dict_context)
    else:
        return redirect('b-login')

# view qui affiche le formulaire d'ajout d'un projet
# TODO : (A REVOIR)
def add_projet(request):
    if request.user.is_authenticated :
        form = ProjetForm()
        return render(request, template_name="backend/projet_add.html", context={'form': form})
    else:
        return redirect('b-login')


