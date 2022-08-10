from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from projets.models import Projet, FORME_AE, FORME_PH, FORME_SOC, FORME_COOP, FORME_AUTRE
from beneficiaires.models import Beneficiaire
from centres.models import Centre, Province, Region
from .forms import LoginForm

def not_found_view(request):
    return redirect('front')

def index(request):
    return render(request, template_name="frontend/index.html")

def espace(request):
    return render(request, template_name="frontend/espace.html")

def not_found(request):
    return render(request, template_name="frontend/404.html")

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

def centre(request, pk=None):
    centre = Centre.objects.get(pk=pk)
    return render(request, template_name="frontend/centre_map.html", context={"centre": centre})

def attestation(request):
    return render(request, template_name="frontend/attestation.html")

def suivi_attestation(request, demande=None):
    return render(request, template_name="frontend/attestation_suivi.html")


def agr(request):
    return render(request, template_name="frontend/agr.html")

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

def details_agr(request, num_demande=None):
    if num_demande :
        projet=Projet.objects.get(pk=num_demande)
        return render(request, template_name="frontend/agr_suivi.html", context={"projet": projet})
    else:
        projets=Projet.objects.all()
        return render(request, template_name="frontend/projets.html", context={"error": True, "projets": projets})

#connexion des membres de la commission
def backlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['is_authenticated'] = True
                return redirect('f-projets')
            else:
                request.session['loginError']=True
                return redirect('b-login')
        else:
            request.session['loginError']=True
            return redirect('b-login')
    else:
        return render(request, template_name="backend/login.html")

#deconnexion des memebres de la commission
def backlogout(request):
    request.session['is_authenticated'] = False
    logout(request)
    return redirect('front')



#affiche la liste des projets
def list_projets(request):
    if request.session.get('is_authenticated', False) :
        projets = Projet.objects.all()
        provinces = Province.objects.all()
        regions = Region.objects.all()
        region_selected = 0
        province_selected = 0
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

        return render(request, template_name="frontend/projets.html", context={"projets": projets, "regions": regions, "provinces": provinces, "province_selected": province_selected, "region_selected": region_selected})
    else:
        return redirect('b-login')


#affiche la liste des projets
def list_psh(request):
    if request.session.get('is_authenticated', False) :
        psh = Beneficiaire.objects.all()
        return render(request, template_name="frontend/psh.html", context={'psh': psh})
    else:
        return redirect('b-login')


def dashboard(request):
    if request.session.get('is_authenticated', False) :
        projets = Projet.objects.all()
        provinces = Province.objects.all()
        regions = Region.objects.all()
        province = 0
        region = 0
        projets_individuels = 0
        projets_collectifs = 0
        try:
            region = int(request.GET['region'])
            if region != 0:
                lieu_region = Region.objects.get(pk=region)
                projets=projets.filter(lieu_region=lieu_region)
                provinces = provinces.filter(region=lieu_region)
        except:
            pass
        try:
            province = int(request.GET['province'])
            if province != 0:
                lieu_province = Province.objects.get(pk=province)
                projets=projets.filter(lieu_province=lieu_province)
        except:
            pass
        # projets par forme juridique
        projets_ae = projets.filter(forme_juridique=FORME_AE).count()
        projets_ph = projets.filter(forme_juridique=FORME_PH).count()
        projets_soc = projets.filter(forme_juridique=FORME_SOC).count()
        projets_coop = projets.filter(forme_juridique=FORME_COOP).count()
        # projets par milieu
        projets_urbain = projets.filter(lieu_commune__milieu=1).count()
        projets_rural = projets.filter(lieu_commune__milieu=2).count()
        dict_context ={
            "projets": projets,
            "regions": regions,
            "provinces": provinces,
            "province_selected": province,
            "region_selected": region,
            "projets_ae": projets_ae,
            "projets_ph": projets_ph,
            "projets_soc": projets_soc,
            "projets_coop": projets_coop,
            "projets_urbain":projets_urbain,
            "projets_rural": projets_rural,
            "projets_collectifs": projets_collectifs,
        }
        return render(request, template_name="backend/dashboard.html", context=dict_context)
    else:
        return redirect('b-login')

from projets.forms import ProjetForm
def add_projet(request):
    if request.user.is_authenticated :
        form = ProjetForm()
        return render(request, template_name="backend/projet_add.html", context={'form': form})
    else:
        return redirect('b-login')


