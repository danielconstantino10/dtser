from django.conf.urls import url
from apps.verbete import views

app_name = 'verbete'

urlpatterns = [
    url(r'^verbete-carta-edit/(?P<pk>\w+)/$', views.editar_verbete_carta, name='verbete_carta_edit'),
    url(r'^verbete-carta-anular/(?P<pk>\w+)/$', views.anular_verbete_carta, name='anular_verbete_carta'),
    url(r'^verbete-carta-prorrogar/(?P<pk>\w+)/$', views.prorrogar_verbete_carta, name='verbete_carta_prorrogar'),
    url(r'^verbete-carta-invoice/(?P<pk>\w+)/$', views.invoice_verbete_carta, name='verbete_carta_invoice'),
    url(r'^verbete-viatura-invoice/(?P<pk>\w+)/$', views.invoice_verbete_viatura, name='verbete_viatura_invoice'),
]