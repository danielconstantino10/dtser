from django.conf.urls import url
from apps.veiculo import views

app_name = 'veiculo'

urlpatterns = [
    url(r'^registo-inicial-viatura/(?P<pk>\w+)/$', views.efectuar_registo_inicial_viatura, name = 'efectuar_registo_inicial_viatura'), 
    url(r'^adicionar_marca/$', views.adicionar_marca, name='marca_add'),
    url(r'^modelo-adicionar/(?P<marca_id>\w)/$', views.adicionar_modelo, name='modelo_add'),
    url(r'^anular_registo_inicial_viatura/(?P<pk>\w)/$', views.anular_registo_inicial_viatura, name='anular_registo_inicial_viatura'),
    url(r'^cor-adicionar/$', views.adicionar_cor, name='cor_add'),
    url(r'^proprietario-viatura-details/(?P<pk>\w+)/$', views.proprietario_viatura_details, name = 'proprietario_viatura_details'), 
    url(r'get_modelo/$', views.get_modelo, name='get_modelo'),
]