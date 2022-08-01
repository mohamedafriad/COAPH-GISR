from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from projets.models import Projet
from beneficiaires.models import Beneficiaire
from centres.models import Centre, Province, Region
from .forms import LoginForm


def index(request):
    return render(request, template_name="frontend/index.html")

def espace(request):
    return render(request, template_name="frontend/espace.html")

def not_found(request):
    return render(request, template_name="frontend/404.html")

def centres(request):
    centres = Centre.objects.all()
    try:
        region = request.GET['region']
        centres=centres.filter(region__pk=region)
    except:
        pass
    try:
        province = request.GET['province']
        centres=centres.filter(province__pk=province)
    except:
        pass
    provinces = Province.objects.all()
    regions = Region.objects.all()
    return render(request, template_name="frontend/centres.html", context={"centres": centres, "regions": regions, "provinces": provinces})

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
        num_demande=request.GET['num_demande']
        projet=Projet.objects.get(pk=num_demande)
        return render(request, template_name="frontend/agr_suivi.html", context={"projet": projet})
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
        try:
            region = int(request.GET['region'])
            if region != 0:
                lieu_region = Region.objects.get(pk=region)
                projets=projets.filter(lieu_region=lieu_region)
                print(projets)
        except:
            pass
        try:
            province = int(request.GET['province'])
            if province != 0:
                lieu_province = Province.objects.get(pk=province)
                projets=projets.filter(lieu_province=lieu_province)
                print(projets)
        except:
            pass
        provinces = Province.objects.all()
        regions = Region.objects.all()
        return render(request, template_name="frontend/projets.html", context={"projets": projets, "regions": regions, "provinces": provinces})
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
        return render(request, template_name="backend/dashboard.html", context={'projets': projets})
    else:
        return redirect('b-login')



