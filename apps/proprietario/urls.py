from django.conf.urls import url
from apps.proprietario import views
from apps.veiculo.views import get_modelo

app_name = 'proprietario'

urlpatterns = [
    url(r'^proprietario-veiculo-list/$', views.proprietario_veiculo_visualizar, name='proprietario_veiculo_visualizar'),
    url(r'^proprietario-carta-list/$', views.proprietario_carta_visualizar, name='proprietario_carta_visualizar'),   
    url(r'^proprietario-veiculo-add/$', views.proprietario_veiculo_add, name='proprietario_veiculo_add'),
    url(r'^proprietario-carta-add/$', views.proprietario_carta_add, name='proprietario_carta_add'),
    url(r'get_modelo/$', get_modelo, name='get_modelo'),
]