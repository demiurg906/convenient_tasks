"""convenient_tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django.contrib.auth.views as auth

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from problems.views import task_search, task_detail, pools, pool_pdf, index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth.LoginView.as_view(template_name='problems/pages/login.html'), name='login'),
    url(r'^logout/$', auth.LogoutView.as_view(next_page='/login'), name='logout'),
    url(r'^tasks/$', task_search),
    url(r'^task/(?P<pk>\d+)/$', task_detail),
    url(r'^pools/$', pools),
    url(r'^pools/pdf/$', pool_pdf),
    url(r'^$', index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
