from django.conf.urls import url
from apps.administration import views

app_name = "administration"
urlpatterns = [
    url(r'^index/$', views.index, name = 'index'),
    url(r'^startup-view/$', views.startups, name = 'startup_view'),
    url(r'^startup-investimento/(?P<startup_id>\w)/$', views.pedido_investimento_startup, name = 'pedido_investimento_startup'),
]