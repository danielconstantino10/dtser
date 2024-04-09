from django.conf.urls import url
from apps.website import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.home_index, name = 'home'),
    url(r'^about/$', views.about, name='about')
    
]