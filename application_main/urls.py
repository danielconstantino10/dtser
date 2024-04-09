"""application_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.website.urls')),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^verbete/', include('apps.verbete.urls'), name='verbete'),
    url(r'^veiculo/', include('apps.veiculo.urls'), name='veiculo'),
    url(r'^administration/', include('apps.administration.urls'), name='administration'),
    url(r'^proprietario/', include('apps.proprietario.urls'), name='proprietario')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
