"""ODtrips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from ODmaps import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^index/', views.index, name='casa'),
	url(r'^test2/', views.test2, name='test2'),
	url(r'^visualizador_n/', views.visualizador_normalizado, name='visualizador_n'),
	url(r'^visualizador/', views.visualizador, name='visualizador'),
	url(r'^$', views.index, name='index'),
]
