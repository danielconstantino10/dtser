from django.conf.urls import url
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^sign_in/$', views.sign_in, name = 'sign_in'),
    url(r'^sair/$', views.sign_out, name = 'sign_out'),
    url(r'^sign-up/$', views.sign_up, name = 'user_add'),
    url(r'^users-list/$', views.visualizar_users, name = 'user_list'), 
]