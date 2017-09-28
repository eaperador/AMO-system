from django.conf.urls import url

import views

urlpatterns = [
    url(r'StateList/$', views.getStateList, name='StateList'),

    url(r'ver_ofertas/$', views.ver_ofertas, name='ver_ofertas'),
    ]
