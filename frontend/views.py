from django.shortcuts import render, get_object_or_404
from projets.models import Projet
from centres.models import Centre, Province, Region


def index(request):
    return render(request, template_name="frontend/index.html")

def espace(request):
    return render(request, template_name="frontend/espace.html")

def not_found(request):
    return render(request, template_name="frontend/404.html")

def centres(request, province=None):
    if province:
        centres=Centre.objects.filter(province__pk=province)
    else:
        centres = Centre.objects.all()
    provinces = Province.objects.all()
    regions = Region.objects.all()
    return render(request, template_name="frontend/centres.html", context={"centres": centres, "regions": regions, "provinces": provinces})

def centre(request, province=None, pk=None):
    centre = Centre.objects.get(pk=pk)
    return render(request, template_name="frontend/centre_map.html", context={"centre": centre})

def attestation(request):
    return render(request, template_name="frontend/attestation.html")

def suivi_attestation(request, demande=None):
    return render(request, template_name="frontend/attestation_suivi.html")


def agr(request):
    return render(request, template_name="frontend/agr.html")

def suivi_agr(request, demande=None):
    if demande:
        try:
            projet=Projet.objects.get(pk=demande)
            return render(request, template_name="frontend/agr_suivi.html", context={"projet": projet})
        except:
            return render(request, template_name="frontend/agr_suivi.html", context={"error": True})
    else:
        return render(request, template_name="frontend/agr_suivi.html")

def aidetech(request):
    return render(request, template_name="frontend/aidetech.html")

def suivi_aidetech(request, demande=None):
    return render(request, template_name="frontend/aidetech_suivi.html")