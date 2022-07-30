"""coaph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
#from attestation import views as attestation_views
from frontend import views as front_views
#from protheses import views as protheses_views
#import xadmin

admin.site.enable_nav_sidebar = False
#router = routers.DefaultRouter()
#router.register(r'attestations', attestation_views.AttestationView, 'attestation')

urlpatterns = [
    #path('xadmin/', include(xadmin.site.urls)),
    #path('admin/', include('djadmin.urls')),
    path('', front_views.index, name="front"),
    #path('api/', include(router.urls)),
    path('espace/', front_views.espace, name="f-espace"),
    path('404/', front_views.not_found, name="f-404"),
    path('coaph/all/', front_views.centres, name="f-centres-tout"),
    path('coaph/<province>/', front_views.centres, name="f-centres"),
    path('coaph/all/<pk>/', front_views.centre, name="f-centre-sanspr"),
    path('coaph/<province>/<pk>/', front_views.centre, name="f-centre"),
    path('attestation/', front_views.attestation, name="f-attestation"),
    path('attestation/suivi/', front_views.suivi_attestation, name="f-suivi-attestation"),
    path('attestation/suivi/<demande>/', front_views.suivi_attestation),
    #path('pdf/<int:attestation_pk>/', attestation_views.GeneratePdf.as_view()),
    path('agr/', front_views.agr, name="f-agr"),
    path('agr/suivi/', front_views.suivi_agr, name="f-suivi-agr"),
    path('agr/suivi/<demande>/', front_views.suivi_agr),
    path('grappelli/', include('grappelli.urls')), # grappelli URL
    #path('admin/attestation/html/', attestation_views.ModelPdf.as_view()),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]